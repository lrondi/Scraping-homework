def scrape():
    from bs4 import BeautifulSoup
    import requests
    import pandas as pd
    from splinter import Browser

    mars_data = {}
    news_url = 'https://mars.nasa.gov/news/'
    news_html = requests.get(news_url)
    news_soup = BeautifulSoup(news_html.text)
    news_response = news_soup.find_all('div', class_='image_and_description_container')
    news_titles = []
    news_p = []
    for i in range(len(news_response)):
        news_titles.append(news_response[i].find_all('img', alt=True)[1].get('alt',''))
        news_p.append(news_response[i].find('div',class_='rollover_description_inner').text.strip())
    news = []
    for i in range(len(news_titles)):
        news.append({'title':news_titles[i],'p':news_p[i]})
    mars_data['news'] = news

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    picture_html = browser.html
    picture_soup = BeautifulSoup(picture_html, 'html.parser')
    browser.click_link_by_partial_text('FULL IMAGE')
    part_url = picture_soup.find_all('a', class_='button fancybox')[0].get('data-fancybox-href')
    image_url = 'https://www.jpl.nasa.gov' + part_url
    mars_data['image'] = image_url

    weather_url =  'https://twitter.com/marswxreport?lang=en'
    weather_html = requests.get(weather_url)
    weather_soup = BeautifulSoup(weather_html.text)
    mars_weather_all = weather_soup.find_all('p', class_='TweetTextSize')
    mars_weather = mars_weather_all[0].text.replace ('\n', ', ')
    mars_weather = mars_weather[:-26]
    mars_data['weather'] = mars_weather

    facts_url = 'https://space-facts.com/mars/'
    facts_html = requests.get(facts_url)
    facts_soup = BeautifulSoup(facts_html.text)
    mars_facts_table = pd.read_html(facts_url)
    mars_facts_table = mars_facts_table[0].rename(columns={0:'Mars profile', 1: ''})
    mars_facts_table = mars_facts_table.set_index('Mars profile')
    mars_facts = mars_facts_table.to_html()
    #mars_facts = mars_facts.replace('\n','')
    mars_data['facts'] = mars_facts

    hemisphere_image_url = [{'title':'Cerberus hemisphere', 'img_url':'https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg'},
    {'title': 'Schiaparelli hemisphere', 'img_url':'https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg'},
    {'title': 'Syrtis major hemisphere', 'img_url':'https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg'},
    {'title': 'Valles Marineris hemisphere', 'img_url':'https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg'}]
    mars_data['hemisphere_img'] = hemisphere_image_url

    return mars_data
    