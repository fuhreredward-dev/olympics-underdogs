official_92 = ['Albania','Andorra','Argentina','Armenia','Australia','Austria','Azerbaijan','Belgium','Benin','Bolivia','Bosnia and Herzegovina','Brazil','Bulgaria','Canada','Chile','China','Colombia','Costa Rica','Croatia','Cyprus','Czech Republic','Denmark','Ecuador','Estonia','Finland','France','Germany','Greece','Great Britain','Guinea-Bissau','Hong Kong','Hungary','Iceland','India','Ireland','Israel','Italy','Jamaica','Japan','Kazakhstan','Kenya','Kosovo','Kyrgyzstan','Latvia','Lebanon','Liechtenstein','Lithuania','Luxembourg','Malaysia','Malta','Mexico','Moldova','Monaco','Mongolia','Montenegro','Morocco','Netherlands','New Zealand','Nigeria','North Macedonia','Norway','Pakistan','Philippines','Poland','Portugal','Puerto Rico','Romania','San Marino','Saudi Arabia','Serbia','Singapore','Slovakia','Slovenia','South Africa','South Korea','Spain','Sweden','Switzerland','Thailand','Timor-Leste','Trinidad and Tobago','Turkey','Ukraine','United Arab Emirates','Uruguay','Uzbekistan','Venezuela']

on_website = ['United States','Canada','Italy','Germany','Switzerland','France','Austria','Czech Republic','Sweden','Finland','Japan','China','Latvia','Norway','Poland','Great Britain','Slovakia','South Korea','Netherlands','Slovenia','Belgium','Kazakhstan','Estonia','Bulgaria','Ukraine','Hungary','Spain','Croatia']

official_set = set(official_92)
website_set = set(on_website)
missing = sorted(official_set - website_set)
extra = sorted(website_set - official_set)

print(f'Total official: {len(official_92)}')
print(f'On website: {len(on_website)}')
print(f'')
print(f'Missing from website (should have cards): {len(missing)}')
for nation in missing:
    print(f'  - {nation}')
print(f'')
print(f'Extra on website (not in official 92): {len(extra)}')
for nation in extra:
    print(f'  - {nation}')
