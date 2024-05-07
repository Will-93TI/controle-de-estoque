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
        name = request.POST.get('name')
        quantity = int(request.POST.get('quantity'))
        expiration_date = request.POST.get('expiration_date')

        # Verifica se já existe um produto com o mesmo nome e validade
        existing_product = Product.objects.filter(name=name, expiration_date=expiration_date).first()

        if existing_product:
            # Se o produto existir, atualize a quantidade adicionando a quantidade fornecida
            existing_product.quantity += quantity
            existing_product.save()
        else:
            # Caso contrário, crie um novo produto
            new_product = Product.objects.create(name=name, quantity=quantity, expiration_date=expiration_date)

        return redirect('menu')
    else:
        # Lógica para exibir o formulário de adicionar produtos
        pass

    # Renderiza o template com o formulário
    return render(request, 'product_create.html')


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