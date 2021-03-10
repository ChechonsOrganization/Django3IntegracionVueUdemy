# creamos para el sitemap
from django.contrib.sitemaps import Sitemap
from listelement.models import Element

class ElementSitemap(Sitemap):
    changefreq = "daily" # daily, yearly, monthly
    priority = 0.5

    def items(self):
        return Element.objects.filter(type=2)
    
    def lastmod(self, obj):
        return obj.updated