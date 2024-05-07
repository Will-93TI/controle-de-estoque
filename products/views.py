from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Product

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('menu')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def menu(request):
    return render(request, 'menu.html')

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('menu')
    else:
        form = ProductForm()
    return render(request, 'product_create.html', {'form': form})

#dar saida nos produtos
def product_output(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        
        # Verifica se a quantidade é válida
        if quantity.isdigit() and int(quantity) > 0:
            product = Product.objects.get(pk=product_id)
            product.quantity -= int(quantity)
            product.save()
            # Redireciona para uma página de sucesso ou para a página inicial
            return redirect('home')
        else:
            # Retorne um erro ou mensagem de validação na mesma página
            pass
    else:
        # Lógica para exibir o formulário de saída de produtos
        pass

    # Renderiza o template com o formulário
    return render(request, 'product_output.html')

#relatorio do que tem em estoque
def stock_report(request):
    products = Product.objects.all()
    # Lógica para gerar o relatório (por exemplo, somar todas as quantidades)
    total_stock = sum(product.quantity for product in products)
    return render(request, 'stock_report.html', {'products': products, 'total_stock': total_stock})