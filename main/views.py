from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Contact, Cart, Customer, Product, Order, Category
import random


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect(admin_view)
        else:
            return redirect(customer)
    else:
        return redirect(customer)


# admin pages and actions
def admin_view(request):
    if request.user.is_superuser:
        contacts = Contact.objects.all().order_by('id').reverse()
        categories = Category.objects.all().order_by('id').reverse()
        pending = Cart.objects.filter(status='pending').order_by('id').reverse()
        categories_no = Category.objects.all().count()
        products = Product.objects.all().order_by('id').reverse()
        products_no = Product.objects.all().count()
        pending_no = Cart.objects.filter(status='pending').count()
        messages_no = contacts.count()

        context = {
            'contacts': contacts,
            'categories': categories,
            'categories_no': categories_no,
            'products': products,
            'products_no': products_no,
            'pending': pending,
            'pending_no': pending_no,
            'messages_no': messages_no,
        }
        return render(request, 'administrator/index.html', context)
    else:
        return redirect('/')


def approve_purchase(request, serial):
    if request.user.is_superuser:
        try:
            item = Cart.objects.get(product_serial=serial)
            item.status = 'approved'
            item.save()
            messages.success(request, "approval successful")
            return redirect(admin_view)
        except:
            messages.error(request, "unknown error")
            return redirect(admin_view)
    else:
        return redirect(home)


def confirm_received(request, serial):
    if request.user.is_authenticated:
        username = request.user.username
        if request.method == 'POST':
            try:
                item = Cart.objects.get(product_serial=serial)
                item.status = 'received'
                item.save()
                messages.success(request, "confirmation successful")
                return redirect(f'/user/{username}')
            except:
                messages.error(request, "unknown error")
                return redirect(f'/user/{username}')
        else:
            return redirect(f'/user/{username}')
    else:
        return redirect(home)


def approve_all(request):
    if request.user.is_superuser:
        try:
            items = Cart.objects.filter(status='pending')
            for item in items:
                item.status = 'approved'
                item.save()
            messages.success(request, "approval successful")
            return redirect(admin_view)
        except:
            messages.error(request, "unknown error")
            return redirect(admin_view)
    else:
        return redirect(home)


def new_product(request):
    if request.user.is_superuser:
        if request.method == 'POST':

            name = request.POST['name']
            category = request.POST['category']
            description = request.POST['description']
            price = request.POST['price']
            image = request.FILES['image']

            if name and category and description and image and price:
                if name == '' or category == '' or description == '' or price == '' or image == '':
                    messages.warning(request, 'Error. Empty field found')
                    return redirect('/')
                else:
                    # generating a serial number
                    def serial_number():
                        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                                   'r',
                                   's', 't', 'u', 'v',
                                   'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                                   'N',
                                   'O', 'P', 'Q', 'R',
                                   'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
                        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

                        let = 4
                        num = 3

                        sequence = random.sample(letters, let)
                        sym = random.sample(numbers, num)
                        sequence.extend(sym)
                        random.shuffle(sequence)
                        serial_num = 'Prod' + ''.join([str(elem) for elem in sequence])  # listToStr
                        check = Product.objects.filter(product_serial=serial_num).exists()
                        if check:
                            return serial_number()
                        else:

                            return serial_num

                    serial = serial_number()
                    p = Product.objects.create(name=name, category=category, price=price, description=description,
                                               image=image,
                                               product_serial=serial)
                    p.save()
                    messages.success(request, 'Product added successfully!!')
                    return redirect('/')
        else:
            messages.error(request, 'fill the product form before submission')
            return redirect('/')
    else:
        return redirect('/')


def new_category(request):
    if request.user.is_superuser:
        if request.method == 'POST':

            category = request.POST['category']
            image = request.FILES['image']

            if category:
                if category == '' or image == '':
                    messages.warning(request, 'Error!1 Empty fields')
                    return redirect('/')
                else:
                    categories = Category.objects.create(name=category, image= image)
                    categories.save()
                    messages.success(request, 'category added successfully!!')
                    return redirect('/')
        else:
            messages.error(request, 'fill the category form to add a new category')
            return redirect('/')
    else:
        return redirect('/')


# end admin pages and actions

def customer(request):
    if request.user.is_superuser:
        return redirect(admin_view)
    elif request.user.is_authenticated:
        member = request.user.username
        cart = Cart.objects.filter(customer_name=member, status='cart')
        cart_no = cart.count()
        # favourite = Favourite.objects.all().order_by('id').reverse()
        # favourite_no = Favourite.objects.all().count()
    else:
        cart = '0'
        cart_no = '0'

    cat = Category.objects.all().order_by('id').reverse()
    gt = cart
    total = 0
    for c in gt:
        try:
            tt = c.total_price
        except:
            tt = "0"
        t = int(tt)
        total += t
    print(total)

    categories = Category.objects.all().order_by('id').reverse()
    products = Product.objects.all().order_by('id').reverse()

    homepage = True
    context = {
        'cart': cart,
        'cart_no': cart_no,
        # 'favourite': favourite,
        # 'favourite_no': favourite_no,
        'categories': categories,
        'products': products,
        'total': total,
        'category': cat,
        'homepage': homepage,
    }
    return render(request, 'users/index.html', context)


def user(request, username):
    if request.user.is_superuser:
        return redirect(admin_view)
    elif request.user.is_authenticated:
        notifications = Contact.objects.filter(name=username).order_by('id').reverse()
        notifications_no = Contact.objects.filter(name=username).count()
        cart = Cart.objects.filter(customer_name=username, status='cart')
        pending = Cart.objects.filter(customer_name=username, status='pending')

        transit = Cart.objects.filter(customer_name=username, status='approved')

        received = Cart.objects.filter(customer_name=username, status='received')

        pending_no = pending.count()
        transit_no = transit.count()
        received_no = received.count()
        cart_no = cart.count()

        cus = Customer.objects.get(phone=username)
        profile = cus.image
        shipping = cus.shipping_address
        balance = cus.account
        id_number = cus.idnumber
        # favourite = Favourite.objects.all().order_by('id').reverse()
        # favourite_no = Favourite.objects.all().count()

        gt = cart
        total = 0
        for c in gt:
            tt = c.total_price
            t = int(tt)
            total += t
        print(total)

        context = {
            'notifications': notifications,
            'notifications_no': notifications_no,
            'pending': pending,
            'transit': transit,
            'received': received,
            'cart': cart,
            'cart_no': cart_no,
            'pending_no': pending_no,
            'transit_no': transit_no,
            'received_no': received_no,

            'profile': profile,
            'shipping': shipping,
            'balance': balance,
            'id_number': id_number,
            'total': total,
        }

        return render(request, 'users/user.html', context)
    else:
        return redirect(customer)


def deposit(request, username):
    if request.user.is_superuser:
        return redirect(admin_view)
    elif request.user.is_authenticated:
        if request.user.username == username:
            if request.method == 'POST':
                amount = request.POST['amount']
                acc = Customer.objects.get(phone=username)
                p = acc.account
                bal = int(p) + int(amount)

                acc.account = bal
                acc.save()
                messages.success(request, "ksh. " + amount + ' deposited successfully!!')
                return redirect('https://stkotgrocery.herokuapp.com/')
            else:
                messages.error(request, "try again")
                return redirect(f'/user/{username}')
        else:
            messages.error(request, "Not permitted to make this transaction")
            return redirect(customer)
    else:
        return redirect('/')


def contact_us(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        try:
            instance = Contact.objects.create(name=name, email=email, subject=subject, message=message)
            instance.save()
        except:
            messages.error(request, 'unknown error')
            return redirect(home)
        messages.success(request, 'message sent successfully')
        return redirect(home)
    else:
        return redirect(home)


def withdraw(request, username):
    if request.user.is_superuser:
        return redirect(admin_view)
    elif request.user.is_authenticated:
        if request.user.username == username:
            if request.method == 'POST':
                amount = request.POST['amount']
                acc = Customer.objects.get(phone=username)
                p = acc.account
                if int(p) <= int(amount) + 20:
                    messages.error(request, "Insufficient amount to withdraw " + amount)
                    return redirect(f'/user/{username}')
                else:
                    bal = int(p) - int(amount)

                    acc.account = bal
                    acc.save()
                    messages.success(request, "ksh. " + amount + ' withdrawal successfully!!')
                    return redirect('https://stkotgrocery.herokuapp.com/')
            else:
                messages.error(request, "try again")
                return redirect(f'/user/{username}')
        else:
            messages.error(request, "Not permitted to make this transaction")
            return redirect(customer)
    else:
        return redirect('/')


# add to cart
def add_to_cart(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST['name']
            p = request.POST['price']
            product = request.POST['product']
            image = request.POST['image']
            quantity = request.POST['quantity']

            price = int(p) * int(quantity)

            cid = Customer.objects.get(phone=request.user.username)
            customer_name = request.user.username
            pid = Product.objects.get(product_serial=product)

            def random_no():
                a = random.random()
                b = a * 1000000000
                c = int(b)
                product_serial = 'Cart' + str(c)
                check = Cart.objects.filter(product_serial=product_serial).exists()
                if check:
                    return random_no()
                else:

                    return product_serial

            serial = random_no()

            cart = Cart.objects.create(customer_name=customer_name, image=image, product_serial=serial,
                                       product_name=name, quantity=quantity, total_price=price, product_id=pid,
                                       customer_id=cid)
            cart.save()
            messages.success(request, name + ' added to cart!!')
            return redirect('/')
        else:
            return redirect(customer)
    else:
        messages.warning(request, 'login first')
        return redirect('/')


def checkout(request, username):
    if request.user.is_authenticated:
        if request.method == 'POST':
            total = request.POST['total']
            member = Customer.objects.get(phone=username)
            bal = member.account
            paid = int(total)
            if paid <= int(bal):
                items = Cart.objects.filter(customer_name=username) and Cart.objects.filter(status='cart')
                for item in items:
                    item.status = 'pending'
                    item.save()
                new_bal = int(bal) - paid
                member.account = new_bal
                member.save()
                messages.success(request, "order placed successful")
                return redirect(f'/user/{username}')
            else:
                messages.error(request, "you have insufficient funds in your account to make this order")
                return redirect(f'/user/{username}')
        else:
            return redirect(customer)
    else:
        messages.warning(request, 'kindly login')
        return redirect('/')


# edit profile
def edit_profile(request, username):
    if request.user.is_authenticated:
        if request.method == 'POST':
            phone = request.POST['phone']
            location = request.POST['location']
            password = request.POST['password']
            password2 = request.POST['password2']
            try:
                pic = request.FILES['pic']
            except:
                member = Customer.objects.get(phone=username)
                pic = member.image
            if password == password2:
                if phone == '' or location == '' or password2 == '' or password2 == '':
                    messages.error(request, 'Fill all the details before submitting')
                    return redirect(f'/user/{username}')
                else:
                    member = Customer.objects.get(phone=username)
                    u_user = User.objects.get(username=username)
                    # username and phone number
                    u_user.username = phone
                    member.phone = phone

                    # password
                    u_user.set_password(password)

                    # location
                    member.shipping_address = location

                    # profile picture
                    member.image = pic

                    # saving the details
                    u_user.save()
                    member.save()
                    messages.success(request, "your profile hs been updated successfully")
                    return redirect(f'/user/{username}')

            else:
                messages.error(request, 'password mismatch. Try again!!')
                return redirect(f'/user/{username}')
        else:
            return redirect(f'/user/{username}')
    else:
        messages.error(request, 'kindly login')
        return redirect('/')


# delete business
def delete_cart(request, prod):
    if request.user.is_authenticated:
        instance = Cart.objects.get(product_serial=prod)
        instance.delete()
        messages.success(request, 'item deleted successfully')
        return redirect(customer)
    else:
        messages.error('Kindly Login')
        return redirect('/')


def delete_category(request, name):
    if request.user.is_superuser:
        instance = Category.objects.get(name=name)
        instance.delete()
        messages.success(request, 'category deleted successfully')
        return redirect(customer)
    else:
        messages.error('Kindly Login')
        return redirect('/')


def contact_view(request):
    if request.method == 'POST':

        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        if name and email and message:
            if name == '' or email == '' or message == '':
                messages.warning(request, 'Message not sent. Empty fields')
                return redirect('/')
            else:
                mail = Contact.objects.create(name=name, email=email, subject=subject, message=message)
                mail.save()
                messages.success(request, 'Message sent successfully!!')
                return redirect('/')
    else:
        return redirect('/')


def signup_view(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        phone = request.POST['phone']
        location = request.POST['location']
        idnumber = request.POST['idnumber']
        gender = request.POST['gender']
        pic = request.FILES['pic']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2 and password != '':
            if firstname and lastname and email and phone and location and idnumber and gender and pic:
                if User.objects.filter(email=email).exists() or Customer.objects.filter(idnumber=idnumber).exists():
                    messages.warning(request, 'Error!!User already exists. Check our details and try again')
                    return redirect('/')
                elif User.objects.filter(username=phone).exists():
                    messages.warning(request, 'Error!!Phone number already registered')
                    return redirect('/')
                else:
                    if email == 'administrator@site.com':
                        super_user = True
                        staff = True
                    else:
                        super_user = False
                        staff = False
                    user = User.objects.create_user(first_name=firstname, last_name=lastname, username=phone,
                                                    is_staff=staff, is_superuser=super_user, email=email,
                                                    password=password)
                    user.save()
                    member = User.objects.get(username=phone)
                    customers = Customer.objects.create(member=member, name=firstname, phone=phone,
                                                        shipping_address=location, image=pic,
                                                        idnumber=idnumber)
                    customers.save()
                    user = auth.authenticate(username=phone, password=password)

                    if user is not None:
                        # correct username and password login the user
                        auth.login(request, user)
                        messages.success(request, 'Registration Successful! Welcome' + request.user.username)
                        return redirect('/')

                    else:
                        messages.error(request, 'Error!! wrong username/password')
                        return redirect('/')

            else:
                messages.error(request, 'Error!! Please fill all the required fields')
                return redirect('/')
        else:
            messages.error(request, 'Error!!Confirmation password error')
            return redirect('/')

    else:
        messages.warning(request, 'Error!! access error')
        return redirect('/')


def login_view(request):
    if request.user.is_authenticated:
        messages.success(request, 'Logged in!!')
        return redirect('/')

    elif request.method == 'POST':
        username = request.POST.get('phone')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # correct username and password login the user
            auth.login(request, user)
            messages.success(request, 'success!!Log in success')
            return redirect('/')

        else:
            messages.error(request, 'Error!! wrong username/password')
            return redirect('/')
    else:
        messages.error(request, 'Error!!page access error')
        return render(request, 'main')


def logout(request):
    auth.logout(request)
    messages.success(request, 'Success!! logout..')
    return redirect('/')
