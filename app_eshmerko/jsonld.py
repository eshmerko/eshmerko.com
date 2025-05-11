import json
from django.urls import reverse
from django.conf import settings

class JSONLDGenerator:
    """
    Базовый класс для генерации JSON-LD структурированных данных
    """
    def __init__(self, request=None):
        self.request = request
        self.site_domain = getattr(settings, 'SITE_DOMAIN', 'eshmerko.com')
        self.site_name = getattr(settings, 'SITE_NAME', 'eshmerko.com')
        self.protocol = 'https'
        
        # Базовые данные о сайте
        self.base_data = {
            "@context": "https://schema.org",
            "@type": "ProfessionalService",
            "name": self.site_name,
            "description": "Профессиональная разработка телеграм ботов, парсеров данных, программного обеспечения, сайтов Django на Python",
            "url": f"{self.protocol}://{self.site_domain}",
            "logo": f"{self.protocol}://{self.site_domain}/static/images/logo.svg",
            "sameAs": ["https://t.me/eshmerko"],
            "contactPoint": {
                "@type": "ContactPoint",
                "telephone": "+375447777710",
                "contactType": "customer service",
                "email": "shmerko2@gmail.com"
            },
            "address": {
                "@type": "PostalAddress",
                "addressCountry": "BY"
            }
        }
        
        # Услуги по умолчанию
        self.default_services = [
            {
                "@type": "Service",
                "name": "Разработка Телеграм Ботов",
                "description": "Создание телеграм ботов любой сложности для автоматизации бизнес-процессов",
                "offers": {
                    "@type": "Offer",
                    "price": "50",
                    "priceCurrency": "USD"
                }
            },
            {
                "@type": "Service",
                "name": "Парсинг Данных",
                "description": "Разработка парсеров данных для извлечения информации из веб-сайтов",
                "offers": {
                    "@type": "Offer",
                    "price": "50",
                    "priceCurrency": "USD"
                }
            },
            {
                "@type": "Service",
                "name": "Разработка ПО",
                "description": "Разработка программного обеспечения на Python для решения различных задач",
                "offers": {
                    "@type": "Offer",
                    "price": "300",
                    "priceCurrency": "USD"
                }
            },
            {
                "@type": "Service",
                "name": "Разработка сайтов на Django",
                "description": "Создаю мощные и безопасные веб-приложения любой сложности на Django",
                "offers": {
                    "@type": "Offer",
                    "price": "500",
                    "priceCurrency": "USD"
                }
            }
        ]
    
    def get_base_data(self):
        """Возвращает базовые данные о сайте"""
        data = self.base_data.copy()
        data["offers"] = {
            "@type": "Offer",
            "itemOffered": self.default_services
        }
        return data
    
    def get_jsonld(self):
        """Возвращает JSON-LD данные по умолчанию"""
        return json.dumps(self.get_base_data(), ensure_ascii=False)


class HomepageJSONLD(JSONLDGenerator):
    """JSON-LD для главной страницы"""
    def get_jsonld(self):
        data = self.get_base_data()
        
        # Добавляем разметку WebSite
        website_data = {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": self.site_name,
            "url": f"{self.protocol}://{self.site_domain}",
            "potentialAction": {
                "@type": "SearchAction",
                "target": f"{self.protocol}://{self.site_domain}/search?q={{search_term_string}}",
                "query-input": "required name=search_term_string"
            }
        }
        
        # Возвращаем массив с двумя объектами JSON-LD
        return json.dumps([data, website_data], ensure_ascii=False)


class ArticleJSONLD(JSONLDGenerator):
    """JSON-LD для страницы статьи"""
    def __init__(self, article, request=None):
        super().__init__(request)
        self.article = article
    
    def get_jsonld(self):
        article_data = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": f"{self.protocol}://{self.site_domain}{self.article.get_absolute_url()}"
            },
            "headline": self.article.title,
            "description": self.article.meta_description,
            "datePublished": self.article.published_date.isoformat(),
            "dateModified": self.article.published_date.isoformat(),
            "author": {
                "@type": "Person",
                "name": "Eshmerko"
            },
            "publisher": {
                "@type": "Organization",
                "name": self.site_name,
                "logo": {
                    "@type": "ImageObject",
                    "url": f"{self.protocol}://{self.site_domain}/static/images/logo.svg"
                }
            }
        }
        
        # Дополнительные метаданные для хлебных крошек
        breadcrumb_data = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Главная",
                    "item": f"{self.protocol}://{self.site_domain}"
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "Блог",
                    "item": f"{self.protocol}://{self.site_domain}/blog/"
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": self.article.title,
                    "item": f"{self.protocol}://{self.site_domain}{self.article.get_absolute_url()}"
                }
            ]
        }
        
        return json.dumps([article_data, breadcrumb_data], ensure_ascii=False)


class ProjectJSONLD(JSONLDGenerator):
    """JSON-LD для страницы проекта"""
    def __init__(self, project, request=None):
        super().__init__(request)
        self.project = project
    
    def get_jsonld(self):
        project_data = {
            "@context": "https://schema.org",
            "@type": "CreativeWork",
            "name": self.project.title,
            "description": self.project.short_description,
            "dateCreated": self.project.completion_date.isoformat(),
            "dateModified": self.project.updated_at.isoformat(),
            "author": {
                "@type": "Person",
                "name": "Eshmerko"
            },
            "creator": {
                "@type": "Organization",
                "name": self.site_name,
                "url": f"{self.protocol}://{self.site_domain}"
            },
            "keywords": self.project.technologies,
            "url": f"{self.protocol}://{self.site_domain}{reverse('project_detail', kwargs={'project_slug': self.project.slug})}"
        }
        
        # Добавляем изображения проекта, если они есть
        if hasattr(self.project, 'images') and self.project.images.exists():
            project_data["image"] = [
                f"{self.protocol}://{self.site_domain}{img.image.url}" 
                for img in self.project.images.all()[:5]  # ограничиваем 5 изображениями
            ]
        
        # Добавляем отзывы, если они есть
        if hasattr(self.project, 'testimonials') and self.project.testimonials.exists():
            project_data["review"] = [
                {
                    "@type": "Review",
                    "author": {
                        "@type": "Person",
                        "name": testimonial.author
                    },
                    "datePublished": testimonial.created_at.isoformat(),
                    "reviewBody": testimonial.text,
                    "name": f"Отзыв о {self.project.title}"
                }
                for testimonial in self.project.testimonials.all()[:3]  # ограничиваем 3 отзывами
            ]
        
        # Хлебные крошки
        breadcrumb_data = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Главная",
                    "item": f"{self.protocol}://{self.site_domain}"
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "Портфолио",
                    "item": f"{self.protocol}://{self.site_domain}/portfolio/"
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": self.project.category.name,
                    "item": f"{self.protocol}://{self.site_domain}{reverse('portfolio_category', kwargs={'slug': self.project.category.slug})}"
                },
                {
                    "@type": "ListItem",
                    "position": 4,
                    "name": self.project.title,
                    "item": f"{self.protocol}://{self.site_domain}{reverse('project_detail', kwargs={'project_slug': self.project.slug})}"
                }
            ]
        }
        
        return json.dumps([project_data, breadcrumb_data], ensure_ascii=False)


class ProgramJSONLD(JSONLDGenerator):
    """JSON-LD для страницы программы"""
    def __init__(self, program, request=None):
        super().__init__(request)
        self.program = program
    
    def get_jsonld(self):
        # Базовая информация о программе
        program_data = {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": self.program.name,
            "description": self.program.description,
            "applicationCategory": "DeveloperApplication",
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "USD",
                "availability": "https://schema.org/InStock"
            },
            "downloadUrl": f"{self.protocol}://{self.site_domain}{reverse('download_program', args=[self.program.id])}",
            "operatingSystem": "Windows, Linux, macOS",
            "softwareVersion": "1.0"
        }
        
        # Если есть обновления, добавляем самую последнюю версию
        latest_update = self.program.updates.filter(is_active=True).order_by('-release_date').first()
        if latest_update:
            program_data["softwareVersion"] = latest_update.version
            program_data["dateModified"] = latest_update.release_date.isoformat()
        
        # Хлебные крошки
        breadcrumb_data = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Главная",
                    "item": f"{self.protocol}://{self.site_domain}"
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "Программы",
                    "item": f"{self.protocol}://{self.site_domain}/software_updates/"
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": self.program.name,
                    "item": f"{self.protocol}://{self.site_domain}{reverse('download_program', args=[self.program.id])}"
                }
            ]
        }
        
        return json.dumps([program_data, breadcrumb_data], ensure_ascii=False)


class BlogListJSONLD(JSONLDGenerator):
    """JSON-LD для страницы списка статей блога"""
    def get_jsonld(self):
        blog_data = {
            "@context": "https://schema.org",
            "@type": "Blog",
            "name": "Блог о программировании на Python",
            "description": "Статьи о разработке программного обеспечения, телеграм ботов и парсеров на Python",
            "url": f"{self.protocol}://{self.site_domain}/blog/",
            "publisher": {
                "@type": "Organization",
                "name": self.site_name,
                "logo": {
                    "@type": "ImageObject",
                    "url": f"{self.protocol}://{self.site_domain}/static/images/logo.svg"
                }
            }
        }
        
        # Хлебные крошки
        breadcrumb_data = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Главная",
                    "item": f"{self.protocol}://{self.site_domain}"
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "Блог",
                    "item": f"{self.protocol}://{self.site_domain}/blog/"
                }
            ]
        }
        
        return json.dumps([blog_data, breadcrumb_data], ensure_ascii=False)


class PortfolioListJSONLD(JSONLDGenerator):
    """JSON-LD для страницы списка проектов портфолио"""
    def get_jsonld(self):
        portfolio_data = {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": "Портфолио проектов",
            "description": "Примеры моих работ: телеграм боты, парсеры данных и программное обеспечение на Python",
            "url": f"{self.protocol}://{self.site_domain}/portfolio/"
        }
        
        # Хлебные крошки
        breadcrumb_data = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Главная",
                    "item": f"{self.protocol}://{self.site_domain}"
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "Портфолио",
                    "item": f"{self.protocol}://{self.site_domain}/portfolio/"
                }
            ]
        }
        
        return json.dumps([portfolio_data, breadcrumb_data], ensure_ascii=False)


class CategoryJSONLD(JSONLDGenerator):
    """JSON-LD для страницы категории проектов"""
    def __init__(self, category, request=None):
        super().__init__(request)
        self.category = category
    
    def get_jsonld(self):
        category_data = {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": f"Проекты категории: {self.category.name}",
            "description": f"Портфолио проектов в категории {self.category.name}",
            "url": f"{self.protocol}://{self.site_domain}{reverse('portfolio_category', kwargs={'slug': self.category.slug})}"
        }
        
        # Хлебные крошки
        breadcrumb_data = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Главная",
                    "item": f"{self.protocol}://{self.site_domain}"
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "Портфолио",
                    "item": f"{self.protocol}://{self.site_domain}/portfolio/"
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": self.category.name,
                    "item": f"{self.protocol}://{self.site_domain}{reverse('portfolio_category', kwargs={'slug': self.category.slug})}"
                }
            ]
        }
        
        return json.dumps([category_data, breadcrumb_data], ensure_ascii=False)