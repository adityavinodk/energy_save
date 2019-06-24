def createInference(category, issues):
    # Creates Inference in the form of a text, according to the categories and issues
    information = ''
    if len(issues)==0: information+='We see no issues at the moment, don\'t forget to regularly reservice your appliance!'
    else: 
        if category == 0:
            information += 'Currently we see issues with ' + \
                ', '.join(issues)+'. These features are the ones consuming a lot of power in the appliance. ' + \
                    'We suggest you service your appliance as soon as possible or if possible, change your appliance and buy one which contains a Energy Star Rating.'
        elif category == 1:
            information += 'Although not major, we see certain issues with ' + \
                ', '.join(issues)+'. We suggest you keep checking for the health and regularly service your appliance.'
        else:
            information += 'Everything looks great!'
    return information
