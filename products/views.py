from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Product
from django.http import JsonResponse

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
            return redirect('stock_report')
    else:
        form = ProductForm()
    return render(request, 'product_create.html', {'form': form})


#dar saida nos produtos
from django.shortcuts import render, redirect
from .models import Product

def product_output(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')

        # Obtém o produto ordenado por data de expiração em ordem decrescente
        product = Product.objects.filter(pk=product_id).order_by('-expiration_date').first()

        if product:
            # Deduz a quantidade do produto
            product.quantity -= int(quantity)

            # Verifique se a quantidade é menor ou igual a zero
            if product.quantity <= 0:
                # Se a quantidade for menor ou igual a zero, exclua o produto
                product.delete()
            else:
                # Caso contrário, salve as alterações no produto
                product.save()

        return redirect('stock_report')
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

