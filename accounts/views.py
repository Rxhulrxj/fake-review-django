from django.contrib import auth
from django.contrib.auth import authenticate
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from .models import Products,Review,Product_Purchase
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords
import numpy as np
import pandas as pd
import sklearn as sk
import pickle
from .forms import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.model_selection import train_test_split
# nltk.download('stopwords')
# set(stopwords.words('english'))
# Create your views here.
def home(request):
    return render(request,'home.html')
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                    form.save()
                    return redirect('login')  
        context = {'form': form}
        return render(request, 'Register.html', context)
def loginpage(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            auth.login(request,user)
            if user.is_superuser == 1 :
                return HttpResponseRedirect('/dashboard')
            else:
                request.session['session_user'] = username
                return HttpResponseRedirect('/productslist')
        else:
            messages.info(request, 'Username or password is incorrect')
            return redirect('login')

    return render(request,'login.html')
@login_required(login_url='login')
def productslist(request):
    products = Products.objects.all()
    user = request.session['session_user']
    return render(request,'product.html',{'products':products,'user':user})
@login_required(login_url='login')
def productpage(request,product_id):
    status=''
    pred = ''
    username = request.session['session_user']
    userid = User.objects.get(username = username).id
    productid = product_id
    detail = Product_Purchase.objects.raw("SELECT * FROM accounts_product_purchase WHERE product_id_id = {} AND purchased_by_id = {}".format(productid,userid))
    if detail:
        status = 'write'
    else:
        status = 'view'
    if status == 'write':
        if request.method == "POST":
            username = request.session['session_user']
            userid = User.objects.get(username=username).id
            comment = request.POST.get('comment')
            reviews = Review()
            reviews.review = comment
            reviews.text_percentage = 50
            reviews.product_id = Products.objects.get(product_id = product_id)
            reviews.review_by = User.objects.get(id = userid)
            reviews.review_date = datetime.date.today()
            if comment !=None or comment != "":
                modelfile="accounts\model\model.pkl"
                csvfile="accounts\dataset\deceptive-opinion.csv"
                model=pickle.load(open(modelfile,'rb'))
                df = pd.read_csv(csvfile)
                df1 = df[['deceptive', 'text']]
                df1.loc[df1['deceptive'] == 'deceptive', 'deceptive'] = 0
                df1.loc[df1['deceptive'] == 'truthful', 'deceptive'] = 1
                X = df1['text']
                Y = np.asarray(df1['deceptive'], dtype = int)
                X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3,random_state=109)
                cv = CountVectorizer()
                x = cv.fit_transform(X_train)
                y = cv.transform(X_test)
                data = [comment]
                vect = cv.transform(data).toarray()
                pred = model.predict(vect)
                if pred == 1:
                    reviews.review_status = 'published'
                    messages.success(request,"🥳🥳🥳Your review has been published")
                    reviews.review_pred = pred
                    reviews.save()
                elif pred == 0:
                    reviews.review_status = 'under_review'
                    messages.success(request,"Your Review is under reviewing.Please Check after some other time.")
                    reviews.review_pred = pred
                    reviews.save()
                reviews.save()
    productdetail=Products.objects.filter(product_id=product_id)
    productreviews = Review.objects.filter(product_id=product_id)
    return render(request,"productdetail.html",{'products':productdetail,'status':status,'reviews':productreviews})
@staff_member_required()
def dashboard(request):
    reviews = Review.objects.all()
    return render(request,'admindashboard.html',{'reviews':reviews})
@staff_member_required()
def publishedreview(request):
    reviews = Review.objects.all()
    return render(request,'publishedreview.html',{'reviews':reviews})
@staff_member_required()
def underreview(request):
    if request.method == "POST":
        review_status = request.POST.get('status')
        review_id = request.POST.get('review_id')
        review = Review.objects.get(review_id=review_id)
        review.review_status = review_status
        review.save()
    reviews = Review.objects.all()
    reviewdata = []
    for item in reviews:
         if item.review_status == 'under_review':
             reviewdata.append(item)
    return render(request,'underreview.html',{'reviews':reviewdata})
@staff_member_required()
def rejectedreview(request):
    if request.method == "POST":
        review_status = request.POST.get('status')
        review_id = request.POST.get('review_id')
        review = Review.objects.get(review_id=review_id)
        review.review_status = review_status
        review.save()
    reviews = Review.objects.all()
    return render(request,'rejectedreview.html',{'reviews':reviews})
def purchaseproduct(request,product_id):
    getuser = request.session['session_user']
    user = User.objects.get(username=getuser).id
    details = Product_Purchase.objects.all()
    print(details)
    purchaseproduct = Product_Purchase()
    purchaseproduct.product_id = Products.objects.get(product_id=product_id)
    purchaseproduct.purchased_by = User.objects.get(id=user)
    purchaseproduct.save()
    messages.success(request,'Product purchased')
    return redirect('productpage',product_id=product_id)
def logout(request):
    auth.logout(request)
    return redirect('home')