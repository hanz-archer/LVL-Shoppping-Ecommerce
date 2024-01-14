from core.models import Product
from django import forms

class AddProductForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Product Name", "class":"form-control"}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Product Description", "class":"form-control"}))
    price = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': "Sale Price", "class":"form-control"}))
    old_price = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': "Old Price", "class":"form-control"}))
    type = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Type of product", "class":"form-control"}))
    stock_count = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': "# of Stocks", "class":"form-control"}))
    tags = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Search Tags", "class":"form-control"}))
    image = forms.ImageField(widget=forms.FileInput(attrs={"class":"form-control"}))

    class Meta:
        model = Product
        fields = [
            'title',
            'image',
            'description',
            'price',
            'old_price',
            'specifications',
            'type',
            'stock_count',
            'tags',
            'digital',
            'category',
        ]

       
