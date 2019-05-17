def scrape():
    from bs4 import BeautifulSoup
    import requests
    import pandas as pd

    news_url = 'https://mars.nasa.gov'
    news_html = requests.get(news_url)
    news_soup = BeautifulSoup(news_html.text)
    response = news_soup.find_all('article', class_='news_teaser')
    news = response[0].find_all('li')
    news_titles = []
    news_p = []
    for i in news:
        news_titles.append(i.find('h3', class_='title').text)
        news_p.append(i.find('img',alt=True)['alt'])
    news_titles = [s.strip() for s in news_titles]
    n = news_p[1]
    news_p[1] = n[1:]
    news_dict = {}
    for i in range(len(news_titles)):
        news_subd = {}
        news_subd['title'] = news_titles[i]
        news_subd['p'] = news_p[i]
        news_dict[i] = news_subd

    weather_url =  'https://twitter.com/marswxreport?lang=en'
    weather_html = requests.get(weather_url)
    weather_soup = BeautifulSoup(weather_html.text)

    mars_weather = weather_soup.find('p', class_='TweetTextSize').text
    mars_weather = mars_weather.replace ('\n', ',')
    mars_weather = mars_weather[:-27]

    facts_url = 'https://space-facts.com/mars/'
    facts_html = requests.get(facts_url)
    facts_soup = BeautifulSoup(facts_html.text)
    table = facts_soup.find('table', class_='tablepress')
    df = pd.read_html(str(table))

    hemisphere_image_url = [{'title':'Cerberus hemisphere', 'img_url':'https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg'},
    {'title': 'Schiaparelli hemisphere', 'img_url':'https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg'},
    {'title': 'Syrtis major hemisphere', 'img_url':'https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg'},
    {'title': 'Valles Marineris hemisphere', 'img_url':'https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg'}]

    mars_data = {}
    mars_data['news'] = news_dict
    mars_data['weather'] = mars_weather
    mars_data['facts'] = df
    mars_data['hemispheres'] = hemisphere_image_url

    return mars_data
