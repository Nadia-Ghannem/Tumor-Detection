from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TumorAnalysis, Patient
from .ai_model import detect_tumor

# Page d'accueil
def home(request):
    return render(request, 'home.html')
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'  # Assurez-vous que ce fichier existe
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Compte créé avec succès ! Vous pouvez maintenant vous connecter.")
            return redirect('login')  # Redirigez vers la vue de connexion après l'inscription
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'  # Assurez-vous que ce fichier existe
# Upload d'image et analyse de la tumeur
@login_required
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']

        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url(filename)

        try:
            result, confidence = detect_tumor(fs.path(filename))
            patient = Patient.objects.filter(user=request.user).first()
            if not patient:
                messages.error(request, "Aucun patient associé à cet utilisateur.")
                return redirect('upload_image')

            TumorAnalysis.objects.create(
                patient=patient,
                image=filename,
                result=result,
                confidence_score=confidence
            )
            return render(request, 'result.html', {
                'result': result,
                'confidence': confidence,
                'image_url': uploaded_file_url
            })
        except Exception as e:
            messages.error(request, f"Erreur lors de l'analyse : {str(e)}")
            return redirect('upload_image')
    return render(request, 'upload.html')
# Consultation des résultats
@login_required

def view_results(request):
    try:
        # Récupérer le patient lié à l'utilisateur connecté
        patient = Patient.objects.filter(user=request.user).first()
        if not patient:
            messages.error(request, "Aucun patient associé à cet utilisateur.")
            return redirect('home')

        # Récupérer les analyses associées au patient
        results = TumorAnalysis.objects.filter(patient=patient)
        if not results.exists():
            messages.info(request, "Aucun résultat trouvé.")
        return render(request, 'results.html', {'results': results})
    except Exception as e:
        messages.error(request, f"Erreur lors de la récupération des résultats : {str(e)}")
        return redirect('home')
