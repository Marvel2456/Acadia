from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from cms.models import SiteSettings
from .models import CustomCakeEnquiry, SurprisePackage, SurprisePackageEnquiry
from .forms import CustomCakeEnquiryForm, SurprisePackageEnquiryForm


def custom_cake_request(request):
    site_settings = SiteSettings.get_settings()
    
    if request.method == 'POST':
        form = CustomCakeEnquiryForm(request.POST, request.FILES)
        if form.is_valid():
            enquiry = form.save()
            if request.headers.get('HX-Request'):
                return render(request, 'enquiries/partials/cake_request_success.html', {
                    'enquiry': enquiry,
                    'site_settings': site_settings,
                })
            messages.success(request, f"Your custom cake request #{enquiry.reference_number} has been received!")
            return redirect('enquiries:cake_confirmation', reference_number=enquiry.reference_number)
        else:
            if request.headers.get('HX-Request'):
                return render(request, 'enquiries/partials/cake_form.html', {
                    'form': form,
                    'site_settings': site_settings,
                })
    else:
        form = CustomCakeEnquiryForm()

    context = {
        'form': form,
        'site_settings': site_settings,
    }
    return render(request, 'enquiries/custom_cake.html', context)


def custom_cake_confirmation(request, reference_number):
    enquiry = get_object_or_404(CustomCakeEnquiry, reference_number=reference_number)
    site_settings = SiteSettings.get_settings()
    return render(request, 'enquiries/cake_confirmation.html', {
        'enquiry': enquiry,
        'site_settings': site_settings,
    })


def surprise_package_list(request):
    packages = SurprisePackage.objects.filter(is_available=True).order_by('display_order', 'name')
    site_settings = SiteSettings.get_settings()
    return render(request, 'enquiries/surprise_packages.html', {
        'packages': packages,
        'site_settings': site_settings,
    })


def surprise_package_detail(request, slug):
    package = get_object_or_404(SurprisePackage, slug=slug, is_available=True)
    site_settings = SiteSettings.get_settings()
    
    if request.method == 'POST':
        form = SurprisePackageEnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save()
            if request.headers.get('HX-Request'):
                return render(request, 'enquiries/partials/package_request_success.html', {
                    'enquiry': enquiry,
                    'package': package,
                    'site_settings': site_settings,
                })
            messages.success(request, f"Your surprise package booking #{enquiry.reference_number} was received!")
            return redirect('enquiries:package_confirmation', reference_number=enquiry.reference_number)
        else:
            if request.headers.get('HX-Request'):
                return render(request, 'enquiries/partials/package_form.html', {
                    'form': form,
                    'package': package,
                })
    else:
        form = SurprisePackageEnquiryForm(initial={'package': package})

    return render(request, 'enquiries/surprise_package_detail.html', {
        'package': package,
        'form': form,
        'site_settings': site_settings,
    })


def surprise_package_confirmation(request, reference_number):
    enquiry = get_object_or_404(SurprisePackageEnquiry, reference_number=reference_number)
    site_settings = SiteSettings.get_settings()
    return render(request, 'enquiries/package_confirmation.html', {
        'enquiry': enquiry,
        'site_settings': site_settings,
    })
