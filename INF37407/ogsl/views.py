from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from typing import List

def root(request: HttpRequest) -> HttpResponse:
    return render(request, 'root.html');

def param(request: HttpRequest, test: str) -> HttpResponse:
    return render(request, 'param.html', {'test': test});

def converter(request: HttpRequest) -> HttpResponse:
    return render(request, 'converter.html');

def getResult(optInitial: str, nInitial: int):
    match optInitial:
        case 'F':
            return 'C', (nInitial - 32) * 5 / 9;
        case 'C':
            return 'F', (nInitial * 9 / 5) + 32;
        case _:
            return None, None;

def convertResult(request: HttpRequest, optInitial: str, nInitial: int) -> HttpResponse:
    optResult, nResult = getResult(optInitial, nInitial);
    return render(request, 'converterResult.html', {
        'nInitial': nInitial,
        'optInitial': optInitial,
        'nResult': nResult,
        'optResult': optResult
    });
