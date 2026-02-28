from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import InventoryItem, Category, Profile
from .forms import InventoryItemForm, UserRegisterForm, ProfileForm, HealthInfoForm
import json
import base64
import numpy as np
import cv2
import os

# ─── Face Login Views ─────────────────────────────────────────────────────────

def login_view(request):
    return render(request, 'inventory/facelogin.html', {})

def logout_view(request):
    logout(request)
    return redirect('login')

@csrf_exempt
def detect_face_view(request):
    if request.method == 'POST':
        from .face_recognition_utils import detect_and_recognize
        data = json.loads(request.body)
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)
        np_arr = np.frombuffer(image_bytes, np.uint8)
        frame_bgr = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

        name, person_info = detect_and_recognize(frame_rgb)

        if name:
            try:
                user = User.objects.get(username=name)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return JsonResponse({'success': True, 'redirect': '/dashboard/'})
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'User not found'})
        else:
            return JsonResponse({'success': False, 'error': 'No face matched'})

@csrf_exempt
def check_face_encoding(request):
    if request.method == 'POST':
        import face_recognition
        photo = request.FILES.get('photo')
        if not photo:
            return JsonResponse({'success': False, 'error': 'No photo provided'})
        image_bytes = photo.read()
        np_arr = np.frombuffer(image_bytes, np.uint8)
        frame_bgr = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(frame_rgb)
        if len(encodings) > 0:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})

# ─── Pill Detection Views ──────────────────────────────────────────────────────

BASE_DIR_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PILL_MODEL_PATH = os.path.join(BASE_DIR_PATH, 'advilrec.pt')

def pill_detection_view(request):
    return render(request, 'inventory/pill_detection.html', {})

@csrf_exempt
def detect_pill_view(request):
    if request.method == 'POST':
        from ultralytics import YOLO
        model = YOLO(PILL_MODEL_PATH)

        data = json.loads(request.body)
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)
        np_arr = np.frombuffer(image_bytes, np.uint8)
        frame_bgr = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        results = model.predict(source=frame_bgr, device='CUDA', conf=0.9) #CHANGE THIS TO GPU ON THE PC PLEASEEEE att. Emilio to Emilio

        detections = []
        annotated_frame = frame_bgr.copy()

        for r in results:
            annotated_frame = r.plot()
            for box in r.boxes:
                cls_id = int(box.cls[0])
                label = model.names[cls_id]
                conf = float(box.conf[0])
                detections.append({'label': label, 'confidence': round(conf * 100, 1)})

        _, buffer = cv2.imencode('.jpg', annotated_frame)
        annotated_b64 = base64.b64encode(buffer).decode('utf-8')

        return JsonResponse({
            'success': True,
            'detections': detections,
            'annotated_image': f'data:image/jpeg;base64,{annotated_b64}'
        })

# ─── Chatbot Views ─────────────────────────────────────────────────────────────

def support_view(request):
    return render(request, 'inventory/support.html', {})

@csrf_exempt
@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        from ollama import chat
        data = json.loads(request.body)
        user_message = data.get('message', '')

        health_context = ""
        if request.user.is_authenticated:
            try:
                profile = Profile.objects.get(user=request.user)
                if any([profile.sex, profile.weight, profile.height, profile.age]):
                    health_context = f"""
The user has provided the following health information:
- Sex: {profile.get_sex_display() if profile.sex else 'Not provided'}
- Weight: {str(profile.weight) + ' kg' if profile.weight else 'Not provided'}
- Height: {str(profile.height) + ' cm' if profile.height else 'Not provided'}
- Age: {profile.age if profile.age else 'Not provided'}

Please take this into account when answering health related questions.
"""
            except Profile.DoesNotExist:
                pass

        base_prompt = f"""You are a helpful health assistant. I am aware you are an AI chatbot, please answer my question as clearly as possible with the information you have available.
{health_context}
User question: """

        response = chat(model='gemma3', messages=[
            {
                'role': 'user',
                'content': base_prompt + user_message,
            },
        ])

        return JsonResponse({
            'success': True,
            'response': response.message.content
        })
    return JsonResponse({'success': False})

# ─── Inventory Views ───────────────────────────────────────────────────────────

class SignUpView(CreateView):
    form_class = UserRegisterForm
    template_name = 'inventory/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        photo = self.request.FILES.get('photo')
        if photo:
            ext = os.path.splitext(photo.name)[1]
            photo.name = f"{self.object.username}{ext}"
            Profile.objects.create(user=self.object, photo=photo)
        else:
            Profile.objects.create(user=self.object)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_form'] = ProfileForm()
        return context

class Index(TemplateView):
    template_name = 'inventory/index.html'

class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'inventory/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = InventoryItem.objects.filter(user=self.request.user)
        context['low_inventory'] = InventoryItem.objects.filter(user=self.request.user, quantity__lte=10)
        return context

@login_required
def information_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = HealthInfoForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('information-page')
    else:
        form = HealthInfoForm(instance=profile)

    return render(request, 'inventory/information.html', {'form': form, 'profile': profile})

class SupportView(LoginRequiredMixin, TemplateView):
    template_name = 'inventory/support.html'

class AddItem(LoginRequiredMixin, CreateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EditItem(LoginRequiredMixin, UpdateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('dashboard')

class DeleteItem(LoginRequiredMixin, DeleteView):
    model = InventoryItem
    template_name = 'inventory/delete_item.html'
    success_url = reverse_lazy('dashboard')