from config.settings import execute_query, execute_query_with_params
from datetime import datetime

def generate_unique_id():
    sql = 'SELECT id FROM article ORDER BY id ASC LIMIT 1 OFFSET (SELECT COUNT(*) - 1 FROM article)'
    id_str = execute_query(sql)[0][0]
    number_str = ''.join(filter(str.isdigit, id_str))
    number = int(number_str)
    prefix = 'AR'
    next_number = number + 1
    padded_number = str(next_number).zfill(2)  # Zero-pad the number if necessary
    return f'{prefix}{padded_number}'

def generate_unique_hots_id():
    sql = 'SELECT id FROM article_hots ORDER BY id ASC LIMIT 1 OFFSET (SELECT COUNT(*) - 1 FROM article_hots)'
    id_str = execute_query(sql)[0][0]
    number_str = ''.join(filter(str.isdigit, id_str))
    number = int(number_str)
    
    prefix = 'HOT'
    next_number = number + 1
    padded_number = str(next_number).zfill(2)
    return f'{prefix}{padded_number}'

def shorten_text(text, max_length):
    return (text[:max_length-3] + '...') if len(text) > max_length else text

class News():
    def article_all(self):
        sql = "select * from article ORDER BY views DESC LIMIT 5;"
        result = execute_query(sql)
        return result
    
    def article_hot(self):
        sql = "SELECT a.*, h.id as hots_id FROM article_hots h JOIN article a ON h.article_id = a.id;"
        result = execute_query(sql)
        return result
    
    def article_new(self):
        sql = "SELECT * FROM article ORDER BY create_date DESC LIMIT 7;"
        result = execute_query(sql)
        return result
    
    def article_bitcoin(self):
        sql = "select * from article where type = 'BITCOIN'"
        result = execute_query(sql)
        return result
    
    def article_altcoin(self):
        sql = "select * from article where type = 'ALTCOIN'"
        result = execute_query(sql)
        return result
    
    def article_nft_gamedefi(self):
        sql = "select * from article where type = 'NFT_GAMEDEFI'"
        result = execute_query(sql)
        return result
    
    def article_defi(self):
        sql = "select * from article where type = 'DEFI'"
        result = execute_query(sql)
        return result
    
    def article_metaverse(self):
        sql = "select * from article where type = 'METAVERSE'"
        result = execute_query(sql)
        return result
    
    def article_phaply(self):
        sql = "select * from article where type = 'PHAPLY'"
        result = execute_query(sql)
        return result
    
    def article_sangiaodich(self):
        sql = "select * from article where type = 'SANGIAODICH'"
        result = execute_query(sql)
        return result
    
    def article_top_views(self):
        sql = "SELECT * FROM article ORDER BY views DESC LIMIT 5;"
        result = execute_query(sql)
        return result

    def article_recently(self):
        sql = "select * from article where type = 'RECENTLY'"
        result = execute_query(sql)
        return result
    
    def article_featured(self):
        sql = "select * from article where type = 'NOIBAT'"
        result = execute_query(sql)
        return result
    
    def article_portal(self):
        sql = "select * from article where type = 'KIENTHUC'"
        result = execute_query(sql)
        return result
    
    def article_airdrop(self):
        sql = "select * from article where type = 'AIRDROP'"
        result = execute_query(sql)
        return result
    
    def article_guidance(self):
        sql = "select * from article where type = 'HUONGDAN'"
        result = execute_query(sql)
        return result
    
    def advertisement(self):
        sql = "select content from advertisement"
        result = execute_query(sql)
        return result
    
    def get_article(self, id):
        sql = "SELECT * FROM article WHERE id = '{0}'".format(id)
        result = execute_query(sql)
        return result[0]
    
    def get_article_all(self):
        sql = "SELECT * FROM article ORDER BY id ASC"
        result = execute_query(sql)
        return result
    
    def get_article_type(self):
        sql = "SELECT * FROM article_type"
        result = execute_query(sql)
        return result
    
    def add_article(self, title, author, content, image_title_url, summary, type):
        # Generate an ID (you may use a more sophisticated method in a real application)
        article_id = generate_unique_id()
        
        title_summary = shorten_text(title, 70)
        
        create_date = datetime.now().strftime('%Y-%m-%d')

        sql = """
            INSERT INTO article (
                id, title, title_summary, image_title_url, author, create_date,
                comment_count, like_count, type, summary, content, views
            ) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', 0, 0, '{}', '{}', '{}', 0)
        """.format(
            article_id, title, title_summary, image_title_url, author, create_date,
            type, summary, content
        )
        
        result = execute_query(sql)
        return result
    
    def delete_article(self, id):
        sql = "DELETE FROM article where id = '{0}'".format(id)
        result = execute_query(sql)
        return result
    
    def update_article(self, title, author, content, image_title_url, summary, type, article_id, createdate):
        sql = """
        UPDATE article
        SET title = '{0}',
            author = '{1}',
            content = '{2}',
            image_title_url = '{3}',
            summary = '{4}',
            type = '{5}',
            create_date = '{6}'
        WHERE id = '{7}';
        """.format(title, author, content, image_title_url, summary, type, createdate, article_id)

        result = execute_query(sql)
        return result
    
    def add_to_hot(self, article_id):
        hot_id = generate_unique_hots_id()
        sql = "INSERT INTO article_hots (id, article_id) VALUES ('{0}', '{1}')".format(hot_id, article_id)
        result = execute_query(sql)
        return result
    
    def delete_to_hot(self, article_id):
        sql = "DELETE from article_hots where article_id = '{0}'".format(article_id)
        result = execute_query(sql)
        return result
    
    def plus_views(self, article_id):
        sql = "UPDATE article SET views = views + 1 WHERE id = '{0}'".format(article_id)
        result = execute_query(sql)
        return result
    
    def count_articles_by_type(self):
        types = ['NOIBAT', 'KIENTHUC', 'AIRDROP', 'HUONGDAN']
        counts = {}

        for article_type in types:
            sql = f"SELECT COUNT(*) FROM article WHERE type = '{article_type}'"
            result = execute_query(sql)
            counts[article_type] = result[0][0] if result else 0

        return counts
        
    