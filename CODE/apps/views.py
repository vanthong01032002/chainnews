import os
from dotenv import load_dotenv
import requests
import binascii
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import base64
from apps.controllers import News

app = Flask(__name__)

def b64encode(value):
    value_with_underscore = str(value).replace('.', '^')
    encoded_value = base64.b64encode(value_with_underscore.encode('utf-8')).decode('utf-8')
    return encoded_value

# Register the custom filter in the Jinja environment
app.jinja_env.filters['b64encode'] = b64encode
app.secret_key = 'cxjeyne7mksl9jsdge88ebvcvm00cnah8asnb522ad'

@app.route('/')
def Home():
    controller = News()
    hots = controller.article_hot()
    news = controller.article_new()
    bitcoins = controller.article_bitcoin()
    altcoins = controller.article_altcoin()
    nft_gamedefis = controller.article_nft_gamedefi()
    defis = controller.article_defi()
    metaverses = controller.article_metaverse()
    phaplys = controller.article_phaply()
    sangiaodichs = controller.article_sangiaodich()
    top_views = controller.article_top_views()
    advertisements = controller.advertisement()
    article_all = controller.article_all()
    recent_articles = session.get('recent_articles', [])
    Categories = controller.count_articles_by_type()
    recentlys = [controller.get_article(article_id) for article_id in recent_articles]
    return render_template('user/pages/home.html', hots=hots, news=news, bitcoins=bitcoins,
                           altcoins=altcoins, nft_gamedefis=nft_gamedefis,
                           defis=defis, metaverses=metaverses,
                           phaplys=phaplys, sangiaodichs=sangiaodichs, top_views = top_views, advertisements =advertisements, article_all=article_all, recentlys=recentlys, categories = Categories)
    

@app.route('/update_data_cmc', methods=['GET'])
def update_data_cmc():
    try:
        api_key = '47d6e24f-c4b0-46f8-a3fb-87f6cf7f5cf5'
        url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?CMC_PRO_API_KEY={api_key}&limit=5'
        response = requests.get(url)
        response.raise_for_status()  # Ném ngoại lệ nếu có lỗi HTTP
        data = response.json()
        top_coins = data['data']
        return jsonify({'status': 'success', 'data': top_coins})
    except requests.exceptions.RequestException as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/featured')
def Featured():
    controller = News()
    hots = controller.article_hot()
    featureds = controller.article_featured()
    return render_template('user/pages/featured.html', featureds = featureds, hots = hots)

@app.route('/portal')
def Portal():
    controller = News()
    portals = controller.article_portal()
    return render_template('user/pages/portal.html', portals = portals)

@app.route('/airdrop')
def Airdrop():
    controller = News()
    airdrops = controller.article_airdrop()
    return render_template('user/pages/airdrop.html', airdrops = airdrops)

@app.route('/guidance')
def Guidance():
    controller = News()
    guidances = controller.article_guidance()
    return render_template('user/pages/guidance.html', guidances = guidances)

@app.route('/<encoded_article_id>')
def Detail(encoded_article_id):
    try:
        # Decode the base64-encoded string
        decoded_value = base64.b64decode(encoded_article_id).decode('utf-8')
        decoded_value = decoded_value.replace('^', '.')
        decoded_article_id = decoded_value
    except (ValueError, binascii.Error):
        # Handle decoding errors (invalid base64 or not an integer)
        return render_template('user/pages/404.html'), 404

    controller = News()
    
    advertisement = controller.advertisement()
    result_view = controller.plus_views(decoded_article_id)
    article = controller.get_article(decoded_article_id)
    
    if article is None:
        # Render 404.html if the article is not found
        return render_template('user/pages/404.html'), 404
    else:
        recent_articles = session.get('recent_articles', [])
        
        if decoded_article_id not in recent_articles:
            recent_articles.insert(0, decoded_article_id)
            if len(recent_articles) > 4:
                recent_articles.pop()
        
        session['recent_articles'] = recent_articles
        
        return render_template('user/pages/detail.html', article=article, advertisement=advertisement)
    

@app.route('/admin')
def admin():
    controller = News()
    article = controller.get_article_all()
    return render_template('admin/pages/dashboard.html', article = article)

@app.route('/admin/dashboard_hot')
def dashboard_hot():
    controller = News()
    article = controller.article_hot()
    return render_template('admin/pages/dashboard_hot.html', article = article)

@app.route('/admin/add_article', methods=['GET', 'POST'])
def add_article():
    controller = News()
    get_type = controller.get_article_type()
    
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        image_title_url = request.form.get('image_title_url')
        article_type = request.form.get('type')
        summary = request.form.get('summary')
        content = request.form.get('content')
        
        success = controller.add_article(title, author, content, image_title_url, summary, article_type)

        if success:
            response_message = {'status': 'success', 'message': 'Article added successfully!'}
            status_code = 200
        else:
            response_message = {'status': 'error', 'message': 'Failed to add the article. Please try again.'}
            status_code = 500
            
        return jsonify(response_message), status_code


    # Render the add_article.html template for GET requests
    return render_template('admin/pages/add_article.html', types = get_type)

@app.route('/admin/delete_article/<id>', methods=['DELETE'])
def delete_article(id):
    controller = News()
    result = controller.delete_article(id)

    if result:
        response_message = {'status': 'success'}
    else:
        response_message = {'status': 'error'}

    return jsonify(response_message)

@app.route('/admin/edit_article/<article_id>')
def edit_article(article_id):
    controller = News()
    get_type = controller.get_article_type()
    article_data = controller.get_article(article_id)
    return render_template('admin/pages/edit_article.html', article=article_data, types = get_type)

@app.route('/admin/update_article/<article_id>', methods=['POST'])
def update_article(article_id):
    title = request.form.get('title')
    author = request.form.get('author')
    image_title_url = request.form.get('image_title_url')
    article_type = request.form.get('type')
    summary = request.form.get('summary')
    createdate = request.form.get('createdate')
    content = request.form.get('content')

    controller = News()
    result = controller.update_article(title, author, content, image_title_url, summary, article_type, article_id, createdate)

    if result:
        response_message = {'status': 'success'}
    else:
        response_message = {'status': 'error'}
        
    return jsonify(response_message)

@app.route('/admin/add_to_hot/<article_id>', methods=['POST'])
def add_to_hot(article_id):
    controller = News()
    result = controller.add_to_hot(article_id)
    print(result)
    if result:
        response_message = {'status': 'success'}
    else:
        response_message = {'status': 'error'}

    return jsonify(response_message)

@app.route('/admin/delete_to_hot/<article_id>', methods=['POST'])
def delete_to_hot(article_id):
    controller = News()
    result = controller.delete_to_hot(article_id)

    if result:
        response_message = {'status': 'success'}
    else:
        response_message = {'status': 'error'}

    return jsonify(response_message)