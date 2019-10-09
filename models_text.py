# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountsProfile(models.Model):
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=500)
    country = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey('AuthUser', models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'accounts_profile'


class AdminPhotosPhotostatistic(models.Model):
    checked_count = models.IntegerField()
    checked_date = models.DateField(unique=True)
    unchecked_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'admin_photos_photostatistic'


class AngSubcategoriesOld(models.Model):
    ang_subcat = models.CharField(max_length=50)
    parent = models.IntegerField()
    ang_sort = models.DecimalField(max_digits=5, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'ang_subcategories_old'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BlogsBlogs(models.Model):
    title = models.CharField(max_length=120)
    slug = models.CharField(unique=True, max_length=255)
    text = models.TextField()
    image = models.CharField(max_length=100, blank=True, null=True)
    publish = models.DateField()
    category = models.ForeignKey('ProductsCategories', models.DO_NOTHING)
    short_desc = models.TextField(blank=True, null=True)
    number_views = models.IntegerField()
    page_description = models.CharField(max_length=500, blank=True, null=True)
    page_title = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'blogs_blogs'


class BlogsOldblogs(models.Model):
    title = models.CharField(max_length=120, blank=True, null=True)
    slug = models.CharField(unique=True, max_length=255, blank=True, null=True)
    short_desc = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=100, blank=True, null=True)
    publish = models.DateField(blank=True, null=True)
    number_views = models.IntegerField(blank=True, null=True)
    page_title = models.CharField(max_length=500, blank=True, null=True)
    page_description = models.CharField(max_length=500, blank=True, null=True)
    category = models.ForeignKey('ProductsCategories', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'blogs_oldblogs'


class CommentsComment(models.Model):
    object_id = models.PositiveIntegerField()
    content = models.TextField()
    timestamp = models.DateTimeField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    user = models.CharField(max_length=100)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comments_comment'


class Dictionary2019(models.Model):
    category_id = models.IntegerField(blank=True, null=True)
    category_name = models.CharField(max_length=255, blank=True, null=True)
    subcat_id = models.CharField(max_length=255, blank=True, null=True)
    subcat_name = models.CharField(max_length=255, blank=True, null=True)
    filter_id = models.CharField(max_length=255, blank=True, null=True)
    filter_name = models.CharField(max_length=255, blank=True, null=True)
    group_id = models.CharField(max_length=255, blank=True, null=True)
    group_name = models.CharField(max_length=255)
    key_plus = models.TextField()
    key_minus = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dictionary_2019'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjangoSite(models.Model):
    domain = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'django_site'


class EmailFormEmailmodel(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=100, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    timestamp = models.DateField()

    class Meta:
        managed = False
        db_table = 'email_form_emailmodel'


class ProductsCart(models.Model):
    cart_total = models.DecimalField(max_digits=9, decimal_places=2)
    timestamp = models.DateField()

    class Meta:
        managed = False
        db_table = 'products_cart'


class ProductsCartItems(models.Model):
    cart = models.ForeignKey(ProductsCart, models.DO_NOTHING)
    cartitem = models.ForeignKey('ProductsCartitem', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'products_cart_items'
        unique_together = (('cart', 'cartitem'),)


class ProductsCartitem(models.Model):
    quantity = models.PositiveIntegerField()
    item_total = models.DecimalField(max_digits=9, decimal_places=2)
    product = models.ForeignKey('ProductsProducts', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'products_cartitem'


class ProductsCategories(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    slug = models.CharField(max_length=500, blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products_categories'


class ProductsCategoriesBack(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    slug = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products_categories_back'


class ProductsCross(models.Model):
    orig_n = models.CharField(max_length=50)
    oem_n = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'products_cross'


class ProductsOrders(models.Model):
    user_bound = models.PositiveIntegerField(blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=500, blank=True, null=True)
    created = models.DateField()
    cart = models.ForeignKey(ProductsCart, models.DO_NOTHING, unique=True)
    comments = models.CharField(max_length=500, blank=True, null=True)
    order_n = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products_orders'


class ProductsProducts(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    cat_n = models.CharField(max_length=255, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    car = models.CharField(max_length=255, blank=True, null=True)
    car_model = models.CharField(max_length=255, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    cond = models.IntegerField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)
    real_weight = models.FloatField(blank=True, null=True)
    seller = models.CharField(max_length=100, blank=True, null=True)
    img_check = models.IntegerField()
    main_img = models.CharField(max_length=500, blank=True, null=True)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'products_products'


class ProductsProductsBack(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    car = models.CharField(max_length=50, blank=True, null=True)
    car_model = models.CharField(max_length=255, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    cond = models.IntegerField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)
    real_weight = models.FloatField(blank=True, null=True)
    cat_n = models.CharField(max_length=255, blank=True, null=True)
    seller = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products_products_back'


class ProductsProductsCat(models.Model):
    products = models.ForeignKey(ProductsProducts, models.DO_NOTHING)
    categories = models.ForeignKey(ProductsCategories, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'products_products_cat'
        unique_together = (('products', 'categories'),)


class ProductsProductsCatBack(models.Model):
    products_id = models.IntegerField()
    categories_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'products_products_cat_back'
        unique_together = (('products_id', 'categories_id'),)


class ProductsProductsCross(models.Model):
    products = models.ForeignKey(ProductsProducts, models.DO_NOTHING)
    cross = models.ForeignKey(ProductsCross, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'products_products_cross'
        unique_together = (('products', 'cross'),)


class StarRatingsRating(models.Model):
    count = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    average = models.DecimalField(max_digits=6, decimal_places=3)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'star_ratings_rating'
        unique_together = (('content_type', 'object_id'),)


class StarRatingsUserrating(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    ip = models.CharField(max_length=39, blank=True, null=True)
    score = models.PositiveSmallIntegerField()
    rating = models.ForeignKey(StarRatingsRating, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'star_ratings_userrating'
        unique_together = (('user', 'rating'),)


class TableRedirectCat(models.Model):
    id_old = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=70, blank=True, null=True)
    id_new = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'table_redirect_cat'
