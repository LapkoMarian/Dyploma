from django.shortcuts import render, redirect


def landing(request):
    return redirect('users:login')
