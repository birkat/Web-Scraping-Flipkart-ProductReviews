from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)

@app.route('/', methods=['GET']) #route to display homepage   
@cross_origin() 
def homePage():
    #return "Hello Scrapper" #used for postman
    return render_template("index.html")

@app.route('/review', methods=['POST', 'GET']) # route to review page
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            #searchstring = request.json['content'] #for postman using json format
            searchstring = request.form['content'].replace(" ","")
            flipkart_url = flipkart_url = "https://www.flipkart.com/search?q=" + searchstring
            response = requests.get(flipkart_url)
            soup = bs(response.content,"html.parser")
            bigboxes = soup.find_all("div", {"class": "_1AtVbE col-12-12"})
            box = bigboxes[2]
            productlink = "https://www.flipkart.com" + box.div.div.div.a['href']
            productName = box.div.div.div.find('div', {'class': '_3pLy-c row'}).div.div.text #this line access product model name sometime its work, it diffents on page html tag
            prodRes = requests.get(productlink)
            prod_html = bs(prodRes.text, "html.parser")

            All_Rev = prod_html.find_all('div', {'class': "col JOpGWq"})  
            rev = []
            for i in All_Rev:
                for j in (i.find_all('a')):
                    rev.append(j.get('href'))
            rev_url = "https://www.flipkart.com" + rev[-1] #extrating nxt page
            rev_link = requests.get(rev_url)
            rev_link_soup = bs(rev_link.content, "html.parser")
            
            #Creating folder of search string and convering into .csv file 
            filename = searchstring + ".csv"
            fw = open(filename, "w")
            headers = "Product, Customer Name, Rating, Heading, Comment \n"
            fw.write(headers)

            #page_revew =[]
            page_num = 1
            flag = 0
            reviews = []
            while page_num <=3: #review goes upto page 3, you can also increase the page number
                if flag == 0:
                    rev_url = "https://www.flipkart.com" + rev[-1]
                else:
                    rev_ = get_next_page_url(rev_url) # return the next page number
                    rev_url = rev_
                    if rev_url:
                        rev_url = "https://www.flipkart.com" + rev_url
                        #print(rev_url)

                rev_link = requests.get(rev_url)
                rev_link_soup = bs(rev_link.content, "html.parser")
                commentboxes = rev_link_soup.find_all('div', {'class': "_1AtVbE col-12-12"})
            
                #review = []
                for comment in range(4, len(commentboxes) - 1):
                    try:
                        name = commentboxes[comment].div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text
                    except:
                        name = "No Name"
                    try:
                        rating = commentboxes[comment].div.div.div.div.div.text
                    except:
                        rating = "No Rating"
                    try:
                        commentHead = commentboxes[comment].div.div.div.p.text
                    except:
                        commentHead = "No Comment Head"
                    try:
                        comtag = commentboxes[comment].div.div.find_all('div', {'class': ''})
                        comm_rev = comtag[0].div.text
                    except:
                        comm_rev = "No Comment"

                    mydict = {"Product": searchstring,"Name": name, "Rating": rating, "CommentHead": commentHead,
                            "Comment": comm_rev}
                    reviews.append(mydict)
                #page_revew.append(review)
                flag = 1
                page_num = page_num + 1
            #return str(page_revew)
            return render_template('results.html', productName = productName, reviews=reviews[0:(len(reviews))])

        except Exception as e:
            print("ERROR OCCUR: ",str(e))
            return "something is wrong1", str(e)
    else:
        return render_template('index.html')        
        
def get_next_page_url(rev_url): # next page number function
    response = requests.get(rev_url)
    soup = bs(response.text, 'html.parser')
    next_page_link = soup.find_all('a', class_='_1LKTO3')[-1]  # Assuming the "Next" link has class '_1LKTO3'
    if next_page_link:
        next_page_url = next_page_link.get('href')
        return next_page_url
    else:
        return None


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8002)

