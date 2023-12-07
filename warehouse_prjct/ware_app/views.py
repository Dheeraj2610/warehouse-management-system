
from django.http import HttpResponseRedirect
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.db.models import F
import re
from django.utils.crypto import get_random_string
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
import random
import string
from django.shortcuts import get_object_or_404, redirect
from django.core.mail import send_mail
from django.urls import reverse
# Create your views here.


def home(request):
    return render(request, 'home.html')


def admin_home(request):

    customer_count = CustomerModel.objects.all().count()
    delivery_count = Delivery.objects.all().count()
    count_product = Product.objects.all().count()
    count_notification = Notification.objects.all().count()
    count_pending_customer = CustomerModel.objects.filter(status=False).count()
    count_pending_delivery = Delivery.objects.filter(status=False).count()
    pending_delivery_count = Order.objects.filter(
        admin_combined_status=Order.PENDING).count()
    delivered_orders_count = Order.objects.filter(
        admin_combined_status=Order.DELIVERED).count()

    context = {

        'customer_count': customer_count,
        'delivery_count': delivery_count,
        'count_product': count_product,
        'count_notification': count_notification,
        'count_pending_customer': count_pending_customer,
        'count_pending_delivery': count_pending_delivery,
        'pending_delivery_count': pending_delivery_count,
        'delivered_orders_count': delivered_orders_count


    }
    return render(request, 'admin_home.html', context)


def signup_page(request):
    return render(request, 'signup_customer.html')


def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('email')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        pan = request.POST.get('pan')
        phone = request.POST.get('phone')
        image = request.FILES.get('file')

        if CustomerModel.objects.filter(cs_email=email).exists():
            messages.info(request, 'Email already exists!')
            return redirect('signup_page')

        confirmation_password = generate_random_password()

        customer = CustomerModel(
            cs_name=name,
            cs_email=email,
            username=username,
            cs_address=address,
            cs_gender=gender,
            cs_pan=pan,
            cs_phone=phone,
            password=confirmation_password,
            cs_image=image,
            status=False
        )
        customer.save()
        Notification.objects.create(
            customer=customer, notification_type='New Customer', notification_for='admin')

        # Sending confirmation email
        send_mail(
            'Confirmation Email',
            f'Your confirmation code: {confirmation_password}',
            'dheerajks.2610@gmail.com',
            [email],
            fail_silently=False,
        )

        return redirect('signin_page')
    else:
        return render(request, 'signup_form.html')


def customer_home(request):
    products = Product.objects.all()
    user_id = request.session.get('user_id')
    customer = get_object_or_404(CustomerModel, id=user_id)

    context = {
        'customer': customer,
        'products': products
    }
    return render(request, 'cus_home.html', context)


def delivery_home(request):
    user_id = request.session.get('user_id')
    delivery_person = get_object_or_404(Delivery, id=user_id)

    assigned_orders_count = Order.objects.filter(
        delivery_person_id=delivery_person.id).count()

    pending_order_count = Order.objects.filter(
        delivery_person_id=delivery_person.id, order_status='pending').count()

    dispatched_order_count = Order.objects.filter(
        delivery_person_id=delivery_person.id, order_status='dispatched').count()

    delivered_order_count = Order.objects.filter(
        delivery_person_id=delivery_person.id, order_status='delivered').count()

    context = {
        'assigned_orders_count': assigned_orders_count,
        'pending_order_count': pending_order_count,
        'dispatched_order_count': dispatched_order_count,
        'delivered_order_count': delivered_order_count
    }
    return render(request, 'del_home.html', context)


def signup_del_page(request):
    return render(request, 'signup_del.html')


def generate_random_password():
    return ''.join(random.choices(string.digits, k=6))


def signup_del(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('email')
        # password = request.POST.get('password')
        phone = request.POST.get('phone')
        image = request.FILES.get('file')

        if Delivery.objects.filter(dl_email=email).exists():
            messages.info(request, 'Email already exists!')
            return redirect('signup_page')

         # Generate a random 6-digit password
        confirmation_password = generate_random_password()

        delivery = Delivery(
            dl_name=name,
            dl_email=email,
            username=username,
            password=confirmation_password,
            status=False,
            dl_phone=phone,
            dl_image=image

        )
        delivery.save()

        # Here you might want to create a Notification for the newly created delivery
        Notification.objects.create(
            delivery=delivery, notification_type='New Delivery', notification_for='admin')

        # Sending confirmation email
        send_mail(
            'Confirmation Email',
            f'Your confirmation code: {confirmation_password}',
            'dheerajks.2610@gmail.com',
            [email],
            fail_silently=False,
        )

        return redirect('signin_page')
    else:
        return render(request, 'signup_form.html')


def signin_page(request):
    return render(request, 'signin.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            # Superuser authenticated
            login(request, user)
            return redirect('admin_home')

        # Check if the provided credentials match the CustomerModel
        customer = CustomerModel.objects.filter(
            username=username).first()

        # Check if the provided credentials match the Delivery model
        delivery = Delivery.objects.filter(
            username=username).first()

        if customer and customer.password == password:
            if customer.status:
                # Perform login for approved Customer and set session variables
                request.session['user_type'] = 'customer'
                request.session['user_id'] = customer.id  # or any identifier
                return redirect('customer_home')
            else:
                # Customer account not approved
                messages.error(request, 'Your account is not approved.')
        elif delivery and delivery.password == password:
            if delivery.status:
                # Perform login for approved Delivery and set session variables
                request.session['user_type'] = 'delivery'
                request.session['user_id'] = delivery.id  # or any identifier
                return redirect('delivery_home')
            else:
                # Delivery account not approved
                messages.error(request, 'Your account is not approved.')
        else:
            # Invalid username or password message
            messages.error(
                request, 'Invalid username or password. Please try again.')

    return render(request, 'signin.html')

# working
# def signin(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)

#         if user is not None and user.is_superuser:
#             # Superuser authenticated
#             login(request, user)
#             return redirect('admin_home')

#         # Check if the provided credentials match the CustomerModel
#         customer = CustomerModel.objects.filter(
#             username=username, password=password, status=True).first()

#         # Check if the provided credentials match the Delivery model
#         delivery = Delivery.objects.filter(
#             username=username, password=password, status=True).first()

#         if customer:
#             # Perform login for Customer and set session variable
#             request.session['user_type'] = 'customer'
#             request.session['user_id'] = customer.id  # or any identifier
#             return redirect('customer_home')
#         elif delivery:
#             # Perform login for Delivery and set session variable
#             request.session['user_type'] = 'delivery'
#             request.session['user_id'] = delivery.id  # or any identifier
#             return redirect('delivery_home')
#         else:
#             messages.error(
#                 request, 'Invalid username or password. Please try again.')
#             return render(request, 'signin.html')

#     return render(request, 'signin.html')


def manage_registrations(request):
    pending_customer = CustomerModel.objects.filter(status=False)
    pending_delivery = Delivery.objects.filter(status=False)
    return render(request, 'manage_regestrations.html', {
        'pending_customer': pending_customer,
        'pending_delivery': pending_delivery,
    })


def approve_customer(request, customer_id):
    customer = get_object_or_404(CustomerModel, pk=customer_id)
    customer.status = True  # Update the status to approved
    customer.save()
    return redirect('manage_registrations')


def approve_delivery(request, delivery_id):
    delivery = get_object_or_404(Delivery, pk=delivery_id)
    delivery.status = True  # Update the status to approved
    delivery.save()
    return redirect('manage_registrations')

# delete customer and delivery


def delete_customer(request, customer_id):
    customer = get_object_or_404(CustomerModel, pk=customer_id)
    # Perform deletion of the customer instance
    customer.delete()
    return redirect('manage_registrations')


def delete_delivery(request, delivery_id):
    delivery = get_object_or_404(Delivery, pk=delivery_id)
    # Perform deletion of the delivery instance
    delivery.delete()
    return redirect('manage_registrations')


def view_notifications(request):
    # Retrieve notifications for new customers and deliveries
    customer_notifications = Notification.objects.filter(
        notification_type='New Customer')
    delivery_notifications = Notification.objects.filter(
        notification_type='New Delivery')

    return render(request, 'notifications.html', {'customer_notifications': customer_notifications, 'delivery_notifications': delivery_notifications})


def delete_customer_notification(request):
    if request.method == 'POST':
        selected_notifications = request.POST.getlist('customer_notification')
        for notification_id in selected_notifications:
            Notification.objects.filter(id=notification_id).delete()
        return redirect('view_notifications')


def delete_delivery_notification(request):
    if request.method == 'POST':
        selected_notifications = request.POST.getlist('delivery_notification')
        for notification_id in selected_notifications:
            Notification.objects.filter(id=notification_id).delete()
        return redirect('view_notifications')


def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        specifications = request.POST.get('specifications')
        price = request.POST.get('price')
        initial_stock_quantity = request.POST.get('initial_stock_quantity')
        photo = request.FILES.get('file')

        new_product = Product.objects.create(
            name=name,
            description=description,
            specifications=specifications,
            price=price,
            initial_stock_quantity=initial_stock_quantity,
            image=photo
        )
        new_product.save()
        messages.success(request, 'Product added sucessfully')
        # Redirect to product list page after adding
        return redirect('add_product')
    else:
        return render(request, 'add_product.html')


def show_product(request):
    product = Product.objects.all()
    return render(request, 'product_details.html', {'product': product})


def edit_product_page(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'edit_products.html', {'product': product})


def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.specifications = request.POST.get('specifications')
        product.price = request.POST.get('price')
        product.initial_stock_quantity = request.POST.get(
            'initial_stock_quantity')
        product.image = request.FILES.get('file')
        product.save()

        return redirect('show_product')

    return render(request, 'edit_products.html', {'product': product})


def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect('show_product')


def view_products(request):
    user_id = request.session.get('user_id')
    customer = get_object_or_404(CustomerModel, id=user_id)
    products = Product.objects.all()
    context = {
        'customer': customer,
        'products': products
    }
    # Fetch all available products from the database
    return render(request, 'product_list.html', context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    # Retrieve the user type and ID from the session
    user_type = request.session.get('user_type')
    user_id = request.session.get('user_id')

    if user_type == 'customer':
        # Retrieve the CustomerModel based on the user_id
        customer = get_object_or_404(CustomerModel, id=user_id)

        # Create or update the CartModel for the customer
        cart_item, created = CartModel.objects.get_or_create(
            customer=customer, product=product)
        messages.success(request, "Item Added to Cart")
        if not created:
            cart_item.quantity += 1  # Or modify the quantity as needed
            cart_item.save()

        # Redirect to the customer's cart page
        return redirect('view_products')

    return redirect('home')

# original without change quantity
# def cart_view(request):
#     user_id = request.session.get('user_id')
#     customer = get_object_or_404(CustomerModel, id=user_id)

#     if user_id:
#         # Assuming the user is logged in
#         customer = get_object_or_404(CustomerModel, id=user_id)
#         cart_items = CartModel.objects.filter(customer=customer)

#         grand_total = 0
#         for item in cart_items:
#             item.total_price = item.product.price * item.quantity
#             item.total_price = item.product.price * item.quantity
#             grand_total += item.total_price

#         context = {
#             'cart_items': cart_items,
#             'grand_total': grand_total,
#             'customer': customer
#         }
#         return render(request, 'cart.html', context)
#     else:
#         # Handle cases where there is no 'user_id' in the session
#         # Redirect to a suitable page or display an appropriate message
#         return redirect('customer_home')


def cart_view(request):
    user_id = request.session.get('user_id')
    customer = get_object_or_404(CustomerModel, id=user_id)

    if user_id:
        customer = get_object_or_404(CustomerModel, id=user_id)
        cart_items = CartModel.objects.filter(customer=customer)

        grand_total = 0
        for item in cart_items:
            item.total_price = item.product.price * item.quantity
            grand_total += item.total_price

        context = {
            'cart_items': cart_items,
            'grand_total': grand_total,
            'customer': customer
        }

        if request.method == 'POST':
            item_id = request.POST.get('item_id')
            new_quantity = int(request.POST.get('quantity'))

            cart_item = get_object_or_404(
                CartModel, id=item_id, customer=customer)
            cart_item.quantity = new_quantity
            cart_item.save()

            return redirect('cart_view')

        return render(request, 'cart.html', context)
    else:
        return redirect('customer_home')


def update_cart_item(request, item_id):
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity'))
        cart_item = get_object_or_404(CartModel, id=item_id)
        cart_item.quantity = new_quantity
        cart_item.save()

    return HttpResponseRedirect(reverse('cart_view'))


def cart_delete(request, pk):
    user_id = request.session.get('user_id')
    if user_id:
        customer = get_object_or_404(CustomerModel, id=user_id)
        cart_item = get_object_or_404(CartModel, id=pk, customer=customer)
        cart_item.delete()
        messages.warning(request, 'Item Deleted Successfully')
        # Redirect back to the cart view after deletion
        return redirect('cart_view')
    else:
        return redirect('customer_home')


def checkout(request):
    user_id = request.session.get('user_id')
    if user_id:
        if request.method == 'POST':
            tracking_id = get_random_string(length=8)
            customer = get_object_or_404(CustomerModel, id=user_id)
            cart_items = CartModel.objects.filter(customer=customer)

            customer_email = customer.cs_email  # Assuming customer has an email field
            subject = 'Order Confirmation'
            message = f'Your order has been placed. Tracking ID: {tracking_id}'
            html_message = render_to_string('order_confirmation_email.html', {
                                            'tracking_id': tracking_id})
            plain_message = strip_tags(html_message)

            # Sending the email
            send_mail(subject, plain_message, None, [
                      customer_email], html_message=html_message)

            for item in cart_items:
                # Check if the product's initial_stock_quantity is available
                if item.product.initial_stock_quantity == 0:
                    messages.error(
                        request, f"{item.product.name} is out of stock.")
                    return redirect('checkout')

                # Check if the ordered quantity is greater than initial_stock_quantity
                if item.quantity > item.product.initial_stock_quantity:
                    messages.error(
                        request, f"Insufficient stock for {item.product.name}.")
                    return redirect('checkout')

                # Reduce the initial_stock_quantity by the ordered quantity
                item.product.initial_stock_quantity = F(
                    'initial_stock_quantity') - item.quantity
                item.product.save()

                # Create order for the cart item
                Order.objects.create(
                    customer=customer,
                    product=item.product,
                    quantity=item.quantity,
                    shipping_method_id=request.POST.get('shipping_method'),
                    tracking_id=tracking_id,
                    # Add other necessary fields for the order
                )

            # Clear the user's cart after placing the order
            CartModel.objects.filter(customer=customer).delete()

            return redirect('order_success')
        else:
            # Fetching current user's cart items and shipping methods
            customer = get_object_or_404(CustomerModel, id=user_id)

            # Retrieve the cart items for the current user
            cart_items = CartModel.objects.filter(customer=customer)

            # Fetch shipping methods
            shipping_methods = ShippingMethod.objects.all()

            # for item in cart_items:
            #     item.total_price = item.product.price * item.quantity
            grand_total = 0
            for item in cart_items:
                item.total_price = item.product.price * item.quantity
                grand_total += item.total_price

            context = {
                'customer': customer,
                'cart_items': cart_items,
                'shipping_methods': shipping_methods,
                'grand_total': grand_total,
            }

            return render(request, 'checkout.html', context)
    else:
        return redirect('customer_home')


def order_success(request):
    return render(request, 'order_success.html')


def checkout_item(request, item_id):
    user_id = request.session.get('user_id')
    if user_id:
        customer = get_object_or_404(CustomerModel, id=user_id)
        cart_item = get_object_or_404(CartModel, id=item_id, customer=customer)

        if request.method == 'POST':

            # Check if the product's initial_stock_quantity is available
            if cart_item.product.initial_stock_quantity == 0:
                # If initial_stock_quantity is 0, show out of stock message
                messages.error(
                    request, f"{cart_item.product.name} is out of stock.")
                # Redirect back to individual checkout page
                return redirect('checkout_item', item_id=item_id)

            # Check if the ordered quantity is greater than initial_stock_quantity
            if cart_item.quantity > cart_item.product.initial_stock_quantity:
                # Show a message indicating insufficient stock
                messages.error(
                    request, f"Insufficient stock for {cart_item.product.name}.")
                # Redirect back to individual checkout page
                return redirect('checkout_item', item_id=item_id)

            # Reduce the initial_stock_quantity by the ordered quantity
            cart_item.product.initial_stock_quantity = F(
                'initial_stock_quantity') - cart_item.quantity
            cart_item.product.save()

            # Create order for the cart item
            tracking_id = get_random_string(length=8)
            customer_email = customer.cs_email  # Assuming customer has an email field
            subject = 'Order Confirmation'
            message = f'Your order has been placed. Tracking ID: {tracking_id}'
            html_message = render_to_string('order_confirmation_email.html', {
                                            'tracking_id': tracking_id})

            plain_message = strip_tags(html_message)

            # Sending the email
            send_mail(subject, plain_message, None, [
                      customer_email], html_message=html_message)

            Order.objects.create(
                customer=customer,
                product=cart_item.product,
                quantity=cart_item.quantity,
                shipping_method_id=request.POST.get('shipping_method'),
                tracking_id=tracking_id,
                # Add other necessary fields for the order
            )

            # Remove the checked out item from the cart
            cart_item.delete()

            return redirect('order_success')  # Redirect to order success page

        else:  # Assuming GET request for showing the checkout page for an individual item
            shipping_methods = ShippingMethod.objects.all()

            total_product_price = cart_item.product.price * cart_item.quantity

            context = {
                'customer': customer,
                'cart_item': cart_item,
                'shipping_methods': shipping_methods,
                'total_product_price': total_product_price,

            }

            return render(request, 'checkout_individual.html', context)
    else:
        return redirect('customer_home')


def view_all_orders(request):
    all_orders = Order.objects.all()

    context = {
        "all_orders": all_orders
    }
    return render(request, 'all_orders.html', context)

# edit delivery person


def edit_order_assign_delivery(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # Fetch all available delivery persons
    delivery_persons = Delivery.objects.all()

    if request.method == 'POST':
        delivery_person_id = request.POST.get('delivery_person')
        if delivery_person_id:
            delivery_person = get_object_or_404(
                Delivery, id=delivery_person_id)
            order.delivery_person = delivery_person
            order.save()
            # Redirect to a suitable page after assigning the delivery person
            # Replace with your URL name for all orders
            return redirect('view_all_orders')

    context = {
        'order': order,
        'delivery_persons': delivery_persons,
    }
    return render(request, 'edit_order_assign_delivery.html', context)


def view_all_orders_delivery(request):
    user_id = request.session.get('user_id')
    delivery_person = get_object_or_404(Delivery, id=user_id)

    # Filter orders based on the current delivery person's ID
    assigned_orders = Order.objects.filter(
        delivery_person_id=delivery_person.id)

    context = {
        "assigned_orders": assigned_orders
    }
    return render(request, 'all_orders_delivery.html', context)


def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        # Retrieve form data to update order details
        status = request.POST.get('order_status')
        location = request.POST.get('location')
        estimated_delivery_time = request.POST.get('estimated_delivery_time')
        location_dispatch = request.POST.get('location_dispatch')
        location_transit = request.POST.get('location_transit')

        # Update order details
        order.order_status = status
        order.location = location
        order.estimated_delivery_time = estimated_delivery_time
        order.location_dispatch = location_dispatch
        order.location_transit = location_transit
        order.save()

        return redirect('view_all_orders_delivery')
 # Pass the order object to the template for rendering the form
    context = {'order': order}
    return render(request, 'edit_order.html', context)


# track order by search
def track_order(request):
    user_id = request.session.get('user_id')
    customer = get_object_or_404(CustomerModel, id=user_id)

    if request.method == 'POST':
        tracking_id = request.POST.get('tracking_id')
        order = Order.objects.filter(tracking_id=tracking_id)

        print(order)
        grand_total = 0
        for item in order:
            item_total = item.product.price * item.quantity
            grand_total += item_total
        context = {
            'customer': customer,
            'order': order,
            'grand_total': grand_total

        }

        return render(request, 'track_order.html', context)
    else:
        # Render an initial template to enter the tracking ID
        return render(request, 'track_order.html')


def order_tracking(request):
    user_id = request.session.get('user_id')
    if user_id:
        # Assuming the user is logged in
        orders = Order.objects.select_related(
            'product').filter(customer_id=user_id)
        product = Product.objects.all()

        context = {
            'orders': orders,
            'product': product
        }
        return render(request, 'order_tracking.html', context)
    else:

        return redirect('customer_home')


def order_tracking_admin(request):
    orders = Order.objects.all()
    customer = CustomerModel.objects.all()
    context = {
        'orders': orders,
        'customer': customer

    }
    return render(request, 'order_tracking_admin.html', context)


def update_client_delivery_status(request, order_id):
    user_id = request.session.get('user_id')
    order = get_object_or_404(Order, id=order_id)

    if order.customer_id == user_id:
        order.client_delivery_status = True
        order.save()
        order.update_admin_combined_status()

        return redirect('order_tracking')


def customer_details_page(request):
    user_id = request.session.get('user_id')
    customer = get_object_or_404(CustomerModel, id=user_id)
    context = {
        'customer': customer
    }
    return render(request, 'customer_details.html', context)


def edit_customer_page(request):
    user_id = request.session.get('user_id')
    customer = get_object_or_404(CustomerModel, id=user_id)
    context = {
        'customer': customer
    }
    return render(request, 'edit_customer.html', context)


def edit_customer(request, pk):
    user_id = request.session.get('user_id')
    # Assuming pk is passed through URL to identify the specific customer
    customer = get_object_or_404(CustomerModel, pk=user_id)

    if request.method == 'POST':
        # Handle form submission and update customer details
        customer.cs_name = request.POST.get('name')
        customer.cs_email = request.POST.get('email')
        customer.cs_address = request.POST.get('address')
        customer.cs_gender = request.POST.get('gender')
        customer.cs_pan = request.POST.get('pan')
        customer.cs_phone = request.POST.get('phone')

        if request.FILES.get('file'):
            customer.cs_image = request.FILES['file']

        customer.save()

        return redirect('customer_details_page')

    # Render the form for editing customer details
    context = {
        'customer': customer
    }
    return render(request, 'edit_customer.html', context)


def customer_reset_password(request):
    user_id = request.session.get('user_id')
    customer = get_object_or_404(CustomerModel, id=user_id)

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        # Retrieve user ID from session
        user_id = request.session.get('user_id')

        if password != confirm_password:
            messages.error(
                request, 'Passwords do not match. Please try again.')
        else:
            if not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
                messages.error(
                    request, 'Password must contain at least 8 characters, including one uppercase letter, one number, and one special character.')
            else:
                # Get the customer based on the user_id stored in the session
                customer = CustomerModel.objects.filter(id=user_id).first()

                if customer:
                    # Update the customer's password
                    customer.password = password
                    customer.save()

                    messages.success(request, 'Password updated successfully.')
                    return redirect('customer_reset_password')
                else:
                    messages.error(request, 'Customer not found.')

    return render(request, 'reset_password.html', {'customer': customer})


def delivery_reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        # Retrieve user ID from session
        user_id = request.session.get('user_id')

        if password != confirm_password:
            messages.error(
                request, 'Passwords do not match. Please try again.')
        else:
            if not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
                messages.error(
                    request, 'Password must contain at least 8 characters, including one uppercase letter, one number, and one special character.')
            else:
                # Get the customer based on the user_id stored in the session
                delivery = Delivery.objects.filter(id=user_id).first()

                if delivery:
                    # Update the customer's password
                    delivery.password = password
                    delivery.save()

                    messages.success(request, 'Password updated successfully.')
                    return redirect('delivery_reset_password')
                else:
                    messages.error(request, 'Customer not found.')

    return render(request, 'pass_reset_del.html')


def customer_details_admin(request):
    customer = CustomerModel.objects.all()
    context = {
        'customer': customer
    }
    return render(request, 'cus_detail_admin.html', context)


def edit_customer_page_admin(request, pk):
    customer = get_object_or_404(CustomerModel, id=pk)
    context = {
        'customer': customer
    }
    return render(request, 'cus_edit_admin.html', context)


def edit_customer_admin(request, pk):

    customer = get_object_or_404(CustomerModel, id=pk)

    if request.method == 'POST':
        # Handle form submission and update customer details
        customer.cs_name = request.POST.get('name')
        customer.cs_email = request.POST.get('email')
        customer.cs_address = request.POST.get('address')
        customer.cs_gender = request.POST.get('gender')
        customer.cs_pan = request.POST.get('pan')
        customer.cs_phone = request.POST.get('phone')

        if request.FILES.get('file'):
            customer.cs_image = request.FILES['file']

        customer.save()
        return redirect('customer_details_admin')

    # Render the form for editing customer details
    context = {
        'customer': customer
    }
    return render(request, 'edit_customer_page_admin', context)


def delete_customer(request, pk):
    customer = get_object_or_404(CustomerModel, id=pk)
    customer.delete()
    return redirect('customer_details_admin')

# delivery user details


def delivery_details_page(request):
    user_id = request.session.get('user_id')
    delivery = get_object_or_404(Delivery, id=user_id)
    context = {
        'delivery': delivery
    }
    return render(request, 'del_details.html', context)


def edit_delivery_page(request):
    user_id = request.session.get('user_id')
    delivery = get_object_or_404(Delivery, id=user_id)
    context = {
        'delivery': delivery
    }
    return render(request, 'edit_delivery.html', context)


def edit_delivery_user(request, pk):
    user_id = request.session.get('user_id')
    # Assuming pk is passed through URL to identify the specific customer
    delivery = get_object_or_404(Delivery, pk=user_id)

    if request.method == 'POST':
        # Handle form submission and update customer details
        delivery.dl_name = request.POST.get('name')
        delivery.dl_email = request.POST.get('email')
        delivery.username = request.POST.get('email')
        delivery.password = request.POST.get('password')
        delivery.dl_phone = request.POST.get('phone')
        delivery.dl_image = request.FILES.get('file')

        if request.FILES.get('file'):
            delivery.dl_image = request.FILES['file']

        delivery.save()
        return redirect('delivery_details_page')

    # Render the form for editing customer details
    context = {
        'delivery': delivery
    }
    return render(request, 'edit_customer.html', context)


def delivery_details_admin(request):
    delivery = Delivery.objects.all()
    context = {
        'delivery': delivery
    }
    return render(request, 'delivery_details_admin.html', context)


def edit_delivery_page_admin(request, pk):
    delivery = get_object_or_404(Delivery, id=pk)
    context = {
        'delivery': delivery
    }
    return render(request, 'delivery_edit_admin.html', context)


def edit_delivery_admin(request, pk):

    delivery = get_object_or_404(Delivery, id=pk)

    if request.method == 'POST':
        # Handle form submission and update customer details
        delivery.dl_name = request.POST.get('name')
        delivery.dl_email = request.POST.get('email')
        delivery.username = request.POST.get('email')
        delivery.password = request.POST.get('password')
        delivery.dl_phone = request.POST.get('phone')
        delivery.dl_image = request.FILES.get('file')

        if request.FILES.get('file'):
            delivery.dl_image = request.FILES['file']

        delivery.save()
        return redirect('delivery_details_admin')

    context = {
        'delivery': delivery
    }
    return render(request, 'edit_delivery_page_admin', context)


def delete_delivery(request, pk):
    delivery = get_object_or_404(Delivery, id=pk)
    delivery.delete()
    return redirect('delivery_details_admin')


def logout_admin(request):
    logout(request)

    return redirect('home')
