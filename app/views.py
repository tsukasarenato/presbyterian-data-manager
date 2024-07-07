from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views import View
from .models import People, Churches
from datetime import datetime

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            return render(request, 'login.html', {'error': 'Usuário ou senha inválidos'})


@method_decorator(login_required, name='dispatch')
class PeopleView(View):

    def get(self, request):

        people = People.objects.all()
        
        return render(request, 'people.html', {'people': people})
    
@method_decorator(login_required, name='dispatch')
class PeopleAddView(View):

    def get(self, request):
        return render(request, 'people_add.html')

    def post(self, request):
        name = request.POST.get('name')
        abbreviated_name = request.POST.get('abbreviated_name')
        phone = request.POST.get('phone')
        date_of_birth = request.POST.get('date_of_birth')
        is_member = request.POST.get('is_member') == 'true'
        status = request.POST.get('status')
        image = request.FILES.get('image')

         # Convert date from dd/mm/yyyy to yyyy-mm-dd
        if date_of_birth:
            date_of_birth = datetime.strptime(date_of_birth, '%d/%m/%Y').date()
        
        # For simplification, I'm using a fixed church. You can modify this as needed.
        church = Churches.objects.first()
        
        person = People.objects.create(
            church=church,
            name=name,
            abbreviated_name=abbreviated_name,
            phone=phone,
            date_of_birth=date_of_birth,
            is_member=is_member,
            status=status,
            image=image
        )
        
        return JsonResponse({'message': 'Person registered successfully!'})

    
@method_decorator(login_required, name='dispatch')
class PeopleEditView(View):

    def get(self, request, pk):
        person = get_object_or_404(People, pk=pk)
        return render(request, 'people_edit.html', {'person': person})
    
    
    def post(self, request, pk):
        person = get_object_or_404(People, pk=pk)
        
        person.name = request.POST.get('name')
        person.abbreviated_name = request.POST.get('abbreviated_name')
        person.phone = request.POST.get('phone')
        person.date_of_birth = request.POST.get('date_of_birth')
        person.is_member = request.POST.get('is_member') == 'true'
        person.status = request.POST.get('status')

        # Convert date from dd/mm/yyyy to yyyy-mm-dd
        if person.date_of_birth:
            person.date_of_birth = datetime.strptime(person.date_of_birth, '%d/%m/%Y').date()
        
        if 'image' in request.FILES:
            person.image = request.FILES.get('image')
        
        person.save()
        
        return JsonResponse({'message': 'Person updated successfully!'})
    
@method_decorator(login_required, name='dispatch')  
class PeopleDeleteView(View):

    def post(self, request, pk):
        person = get_object_or_404(People, pk=pk)
        person.delete()
        return JsonResponse({'message': 'Person deleted successfully!'})
    
    def get(self, request):
        return JsonResponse({'error': 'Method not allowed'}, status=405)
