SELECTORS = {
        # search page
        'search_content': '//main/div[2]//h2',
        'search_input': '//input[@id="location-typeahead-home-input"]',
        'search_button': '//main//button[contains(text(), "Find Food")]',

        # search result page
        'show_more_button': '//button[text()="Show more"]',
        'restaurant_link': '//a[contains(@href, "food")]',
        'popular_food_near_you' : "//div[@class='ev au av ew']//text()[contains(., 'Popular Near You')]//ancestor::div[@class='ev au av ew']/following-sibling::div/a/@href",

        # restaurant page
        'rest_name': '//main/div[1]/div[1]/div[1]/div[2]/div/div[2]/h1/text()',
        'food_type': "//div[@class='cd d2 bs as dl']/text()",
        'delivery_time': "//div[@aria-hidden='true'  and @class='au aw'][1]/text()",
        'delivery_fee': "//div[@aria-hidden='true'  and @class='au aw'][2]/text()",
        'rating': "//div[@class='as']/text()",
        
        # 'caption': '//main/div[1]/div[1]/div[1]/div[2]/div/div[2]/div[1]/text()',
        'address': '//main/div[1]/div[1]/div[1]/div[2]/div/div[2]/p//text()',

        'section': '//main/div[2]/ul/li',
        'section_name': './h2/text()',

        'item': './ul/li',
        'item_name': './div/div/div/div[1]/h4//text()',
        'item_text_areas': './div/div/div/div[1]/div/div//text()'
    }