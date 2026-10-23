import os
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from catalog.models import Category, Occasion, Product, ProductVariation
from enquiries.models import SurprisePackage
from cms.models import SiteSettings, HeroSection, PromotionalBanner, Testimonial


class Command(BaseCommand):
    help = "Seeds initial database for Acadia bakery, food, and surprise packages"

    def handle(self, *args, **options):
        self.stdout.write("Seeding Acadia database...")

        # 1. Site Settings
        site_settings, created = SiteSettings.objects.get_or_create(id=1)
        site_settings.business_name = "Acadia"
        site_settings.tagline = "A Little Sweetness. A Lot of Love."
        site_settings.phone = "+234 812 345 6789"
        site_settings.whatsapp_number = "2348123456789"
        site_settings.email = "orders@acadiabakes.com"
        site_settings.address = "Plot 12 Admiralty Way, Lekki Phase 1, Lagos, Nigeria"
        site_settings.opening_hours = "Mon – Sat: 8:00 AM – 8:00 PM | Sun: 11:00 AM – 6:00 PM"
        site_settings.active_logo = "script_character"
        site_settings.lead_time_cake_days = 2
        site_settings.lead_time_packages_hours = 24
        site_settings.standard_delivery_fee = Decimal('2500.00')
        site_settings.free_delivery_threshold = Decimal('60000.00')
        site_settings.bank_name = "Guaranty Trust Bank (GTB)"
        site_settings.account_number = "0123456789"
        site_settings.account_name = "Acadia Bakery & Confectionery Ltd"
        site_settings.allow_bank_transfer = True
        site_settings.allow_paystack = True
        site_settings.save()
        self.stdout.write("✓ Site settings configured")

        # 2. Hero Section
        hero, _ = HeroSection.objects.get_or_create(id=1)
        hero.headline = "A Little Sweetness. A Lot of Love."
        hero.subheadline = "From freshly baked treats and delicious meals to beautiful celebration cakes and thoughtful surprise packages, Acadia makes every moment taste special."
        hero.badge_text = "Handcrafted Fresh Daily in Lagos"
        hero.primary_cta_text = "Explore Our Menu"
        hero.primary_cta_url = "/shop/"
        hero.secondary_cta_text = "Order a Custom Cake"
        hero.secondary_cta_url = "/custom-cakes/"
        hero.is_active = True
        hero.save()
        self.stdout.write("✓ Hero section configured")

        # 3. Occasions
        occasions_data = [
            ("Birthdays", "birthdays", "Make their birthday unforgettable with artisan cakes and personalized surprises."),
            ("Weddings & Anniversaries", "weddings-anniversaries", "Romantic, bespoke tiered cakes crafted for your lifetime memories."),
            ("Graduations", "graduations", "Celebrate milestone academic and career achievements with grand confections."),
            ("Celebrations & Parties", "celebrations", "Sweet treats, cupcakes, and savory bistro platters for party crowds."),
            ("Corporate Gifts", "corporate-gifts", "Impress clients and reward hardworking teams with gourmet bakery hampers."),
            ("Just Because", "just-because", "Because someone special deserves a sweet surprise today for no reason at all!"),
        ]
        occasions_map = {}
        for name, slug, desc in occasions_data:
            occ, _ = Occasion.objects.get_or_create(slug=slug, defaults={'name': name, 'description': desc})
            occasions_map[slug] = occ
        self.stdout.write("✓ Occasions seeded")

        # 4. Categories
        categories_data = [
            ("Freshly Baked Treats", "baked-treats", "Golden flaky croissants, brioche buns, savory pies, and artisan morning pastries.", "pastry", "categories/baked-treats.jpg"),
            ("Delicious Meals", "delicious-meals", "Freshly prepared cooked meals, comforting bistro dishes, and savory party favorites.", "meal", "categories/cooked-meals.jpg"),
            ("Custom Cakes", "custom-cakes", "Creative bespoke cakes for birthdays, weddings, anniversaries, and grand milestones.", "cake", "categories/custom-cakes.jpg"),
            ("Sweet Treats & Desserts", "sweet-treats", "Delicate bento cakes, gourmet cupcakes, cookies, tarts, and dessert platters.", "dessert", "categories/desserts.jpg"),
            ("Surprise Packages", "surprise-packages", "Thoughtful curated gift hampers packed with treats, cards, and celebratory touches.", "gift", "categories/surprise-packages.jpg"),
        ]
        categories_map = {}
        for name, slug, desc, icon, img_rel in categories_data:
            cat, _ = Category.objects.get_or_create(slug=slug, defaults={
                'name': name,
                'description': desc,
                'icon_name': icon,
            })
            cat.image = img_rel
            cat.save()
            categories_map[slug] = cat
        self.stdout.write("✓ Categories seeded")

        # 5. Products
        products_data = [
            {
                "name": "Signature 3-Tier Pastel Celebration Cake",
                "slug": "signature-3-tier-pastel-celebration-cake",
                "category": categories_map["custom-cakes"],
                "price": Decimal("75000.00"),
                "short_description": "Exquisite handcrafted multi-tier cake with pastel watercolour buttercream, gold leaf, and fresh floral accents.",
                "full_description": "Our show-stopping centrepiece cake designed for luxury weddings, milestone birthdays, and unforgettable celebrations. Made with layers of moist sponge filled with velvety Swiss meringue buttercream and adorned with delicate edible 24k gold leaf and fresh garden florals.",
                "is_featured": True,
                "is_bestseller": True,
                "lead_time_hours": 48,
                "servings_or_size": "Serves 35–45 guests",
                "image_path": "media/products/custom-celebration-cake.jpg",
                "occasions": ["birthdays", "weddings-anniversaries", "celebrations"],
                "variations": [
                    ("Standard 2-Tier (25 Servings)", Decimal("0.00")),
                    ("Grand 3-Tier (45 Servings)", Decimal("20000.00")),
                ]
            },
            {
                "name": "Sweet Heart Pastel Bento Cake",
                "slug": "sweet-heart-pastel-bento-cake",
                "category": categories_map["sweet-treats"],
                "price": Decimal("14500.00"),
                "short_description": "Adorable 4-inch Korean-style mini bento cake packed in an eco clamshell box with custom message piping.",
                "full_description": "Perfect for intimate moments, couple surprises, and cute birthday photos. Our viral Bento Cakes come with soft sponge, silky vanilla cream, vintage cherry accents, and your personalized piped message.",
                "is_featured": True,
                "is_bestseller": True,
                "lead_time_hours": 24,
                "servings_or_size": "Serves 1–2",
                "image_path": "media/products/pastel-bento-cupcakes.jpg",
                "occasions": ["birthdays", "just-because"],
                "variations": [
                    ("Vanilla Bean & Strawberry Compote", Decimal("0.00")),
                    ("Belgian Chocolate Fudge", Decimal("1500.00")),
                    ("Red Velvet Cream Cheese", Decimal("1500.00")),
                ]
            },
            {
                "name": "Artisanal Butter Croissant & Brioche Box",
                "slug": "artisanal-butter-croissant-box",
                "category": categories_map["baked-treats"],
                "price": Decimal("9500.00"),
                "short_description": "A box of 4 flaky French butter croissants, pain au chocolat, and cinnamon swirl brioche pastries.",
                "full_description": "Laminated by hand and baked to golden perfection every morning. Features 2 classic flaky butter croissants, 1 double-chocolate pain au chocolat, and 1 spiced cinnamon roll glazed with vanilla icing.",
                "is_featured": True,
                "is_bestseller": True,
                "lead_time_hours": 4,
                "servings_or_size": "Box of 4 pastries",
                "image_path": "media/products/artisan-croissant-box.jpg",
                "occasions": ["celebrations", "just-because", "corporate-gifts"],
                "variations": [
                    ("Box of 4 (Mixed Selection)", Decimal("0.00")),
                    ("Box of 8 (Party Sharing)", Decimal("8500.00")),
                ]
            },
            {
                "name": "Bistro Smoky Jollof Rice & Roasted Spiced Chicken",
                "slug": "bistro-smoky-jollof-rice-roasted-chicken",
                "category": categories_map["delicious-meals"],
                "price": Decimal("8500.00"),
                "short_description": "Signature firewood-style party jollof served with succulent spiced quarter chicken, sweet plantains (dodo), and fresh salad.",
                "full_description": "Cooked food just right for your taste buds! Long-grain rice slow-cooked in a rich smoky tomato-pepper reduction, paired with tender herb-marinated roasted chicken and golden sweet fried plantains.",
                "is_featured": True,
                "is_bestseller": True,
                "lead_time_hours": 4,
                "servings_or_size": "1 Generous Portion",
                "image_path": "media/products/bistro-jollof-chicken.jpg",
                "occasions": ["celebrations", "just-because"],
                "variations": [
                    ("Quarter Chicken Option", Decimal("0.00")),
                    ("Jumbo Prawns & Beef Suya Combo", Decimal("4000.00")),
                ]
            },
            {
                "name": "Gourmet Frosted Cupcakes Box of 6",
                "slug": "gourmet-frosted-cupcakes-box-of-6",
                "category": categories_map["sweet-treats"],
                "price": Decimal("16500.00"),
                "short_description": "Half-dozen fluffy cupcakes frosted with pastel buttercream swirls, sprinkles, and edible floral pearls.",
                "full_description": "An assortment of Acadia's signature cupcake flavours: 2 Red Velvet with cream cheese swirl, 2 Vanilla Bean with pastel buttercream, and 2 Triple Chocolate Fudge.",
                "is_featured": True,
                "is_bestseller": False,
                "lead_time_hours": 12,
                "servings_or_size": "Box of 6 Cupcakes",
                "image_path": "media/products/pastel-bento-cupcakes.jpg",
                "occasions": ["birthdays", "celebrations", "corporate-gifts"],
                "variations": [
                    ("Box of 6 (Classic Assortment)", Decimal("0.00")),
                    ("Box of 12 (Celebration Box)", Decimal("14000.00")),
                ]
            },
            {
                "name": "Artisanal Rich Butter Brioche Loaf & Pies",
                "slug": "artisanal-butter-brioche-loaf-pies",
                "category": categories_map["baked-treats"],
                "price": Decimal("7500.00"),
                "short_description": "Pillowy, golden brioche loaf baked fresh daily alongside 2 signature flaky beef savoury pies.",
                "full_description": "Our signature morning bread made with 100% pure butter and eggs for an irresistible feather-light crumb. Accompanied by two hearty, spiced minced beef pies wrapped in crisp, buttery pastry.",
                "is_featured": True,
                "is_bestseller": False,
                "lead_time_hours": 3,
                "servings_or_size": "1 Loaf + 2 Savoury Pies",
                "image_path": "media/products/artisan-croissant-box.jpg",
                "occasions": ["just-because", "celebrations"],
                "variations": [
                    ("Standard Bundle (1 Loaf + 2 Pies)", Decimal("0.00")),
                    ("Family Feast (2 Loaves + 4 Pies)", Decimal("6800.00")),
                ]
            },
            {
                "name": "Creamy Tuscan Chicken & Alfredo Penne",
                "slug": "creamy-tuscan-chicken-alfredo-penne",
                "category": categories_map["delicious-meals"],
                "price": Decimal("9500.00"),
                "short_description": "Al dente penne folded in a velvety parmesan cream sauce, sun-dried tomatoes, and tender grilled herb chicken.",
                "full_description": "Warm, comforting cooked food crafted with the finest ingredients. Grilled breast of chicken seasoned with Mediterranean herbs, served atop al dente penne pasta in our house-made rich garlic parmesan sauce.",
                "is_featured": True,
                "is_bestseller": True,
                "lead_time_hours": 2,
                "servings_or_size": "1 Generous Bistro Bowl",
                "image_path": "media/products/bistro-jollof-chicken.jpg",
                "occasions": ["celebrations", "just-because"],
                "variations": [
                    ("Grilled Herb Chicken", Decimal("0.00")),
                    ("Seared Garlic Butter Prawns", Decimal("3500.00")),
                ]
            },
        ]

        for p_data in products_data:
            prod, created = Product.objects.get_or_create(
                slug=p_data["slug"],
                defaults={
                    "name": p_data["name"],
                    "category": p_data["category"],
                    "price": p_data["price"],
                    "short_description": p_data["short_description"],
                    "full_description": p_data["full_description"],
                    "is_featured": p_data["is_featured"],
                    "is_bestseller": p_data["is_bestseller"],
                    "lead_time_hours": p_data["lead_time_hours"],
                    "servings_or_size": p_data["servings_or_size"],
                }
            )
            # Add image
            img_path = os.path.join(settings.BASE_DIR, p_data["image_path"])
            if os.path.exists(img_path):
                prod.image = p_data["image_path"].replace('media/', '')
                prod.save()

            # Add occasions
            for occ_slug in p_data["occasions"]:
                if occ_slug in occasions_map:
                    prod.occasions.add(occasions_map[occ_slug])

            # Add variations
            for v_name, v_price in p_data["variations"]:
                ProductVariation.objects.get_or_create(
                    product=prod,
                    name=v_name,
                    defaults={'price_modifier': v_price, 'is_available': True}
                )

        self.stdout.write("✓ Products and variations seeded")

        # 6. Surprise Packages
        packages_data = [
            {
                "name": "Royal Birthday Bliss Surprise Hamper",
                "slug": "royal-birthday-bliss-surprise-hamper",
                "starting_price": Decimal("65000.00"),
                "short_description": "Our most popular surprise hamper with a pastel bento cake, 6 cupcakes, chocolates, handwritten card, and festive ribbons.",
                "full_description": "Delight your loved one with an unforgettable morning delivery. Includes a customized message bento cake, 6 assorted cupcakes, luxury gold-foiled artisan chocolates, a fragrant mini scented candle, celebratory confetti balloons, and a wax-sealed handwritten message card.",
                "included_items": "Pastel Celebration Bento Cake (Serves 1–2)\nBox of 6 Gourmet Frosted Cupcakes\nLuxury Belgian Chocolate Pralines Box\nHandcrafted Wax-Sealed Calligraphy Card\nScented Aroma Candle & Party Confetti Horn\nSatin Ribbon Woven Gift Basket Presentation",
                "is_featured": True,
                "is_customizable": True,
                "lead_time_hours": 24,
                "image_path": "media/packages/royal-surprise-box.jpg",
                "occasions": ["birthdays", "celebrations", "just-because"],
            },
            {
                "name": "Sweet Romance & Anniversary Package",
                "slug": "sweet-romance-anniversary-package",
                "starting_price": Decimal("75000.00"),
                "short_description": "A heart-stirring romance package with velvet cake, fresh roses, sparkling juice/wine, and sweet chocolates.",
                "full_description": "Express your deepest affection with Acadia's signature romance package. Delivered discreetly or presented as a grand reveal at home or work.",
                "included_items": "6-inch Red Velvet Heart Cake with Cream Cheese\nMini Bouquet of Fresh Pink & Peach Roses\nBottle of Premium Non-Alcoholic Sparkling Wine\nBox of Handcrafted Truffles\nPersonal Love Letter on Parchment Paper",
                "is_featured": True,
                "is_customizable": True,
                "lead_time_hours": 24,
                "image_path": "media/packages/royal-surprise-box.jpg",
                "occasions": ["weddings-anniversaries", "just-because"],
            },
            {
                "name": "Sunshine 'Just Because' Hamper",
                "slug": "sunshine-just-because-hamper",
                "starting_price": Decimal("38000.00"),
                "short_description": "Brighten someone's day unexpectedly with a delightful box of bakery pastries, sweet cupcakes, and a warm note.",
                "full_description": "Sometimes the best gift is the one they never saw coming. Packed with fresh morning pastries, comforting cupcakes, and uplifting cheer.",
                "included_items": "Box of 4 Flaky Breakfast Croissants & Brioche\nBox of 4 Assorted Fruity Cupcakes\nArtisan Granola & Honey Jar\nCustom Cheerful Greeting Note",
                "is_featured": False,
                "is_customizable": True,
                "lead_time_hours": 12,
                "image_path": "media/packages/royal-surprise-box.jpg",
                "occasions": ["just-because", "corporate-gifts"],
            },
        ]

        for pkg_data in packages_data:
            pkg, _ = SurprisePackage.objects.get_or_create(
                slug=pkg_data["slug"],
                defaults={
                    "name": pkg_data["name"],
                    "starting_price": pkg_data["starting_price"],
                    "short_description": pkg_data["short_description"],
                    "full_description": pkg_data["full_description"],
                    "included_items": pkg_data["included_items"],
                    "is_featured": pkg_data["is_featured"],
                    "is_customizable": pkg_data["is_customizable"],
                    "lead_time_hours": pkg_data["lead_time_hours"],
                }
            )
            img_path = os.path.join(settings.BASE_DIR, pkg_data["image_path"])
            if os.path.exists(img_path):
                pkg.image = pkg_data["image_path"].replace('media/', '')
                pkg.save()

            for occ_slug in pkg_data["occasions"]:
                if occ_slug in occasions_map:
                    pkg.occasions.add(occasions_map[occ_slug])

        self.stdout.write("✓ Surprise packages seeded")

        # 7. Promotional Banner
        banner, _ = PromotionalBanner.objects.get_or_create(id=1, defaults={
            "title": "Fresh Morning Bakes & Jollof Bistro Ready for Dispatch!",
            "subtitle": "Order before 11:00 AM for same-day delivery across Lagos. Free delivery on orders over ₦60,000.",
            "button_text": "Order Fresh Today",
            "button_url": "/shop/",
            "bg_style": "lime",
            "is_active": True,
        })
        self.stdout.write("✓ Promotional banner configured")

        self.stdout.write(self.style.SUCCESS("★ Acadia database successfully seeded!"))
