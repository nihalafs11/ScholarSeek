from django.shortcuts import render
import pyterrier as pt

if not pt.started():
    pt.init()
