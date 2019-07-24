from django.shortcuts import render
from django.http import HttpResponse

# Include the `fusioncharts.py` file which has required functions to embed the charts in html page
from .fusioncharts import FusionCharts

# Loading Data from a Static JSON String
# The `chart` method is defined to load chart data from an JSON string.

from django.shortcuts import render
from django.http import HttpResponse
from collections import OrderedDict


def myFirstMap(request):
    print("My first map")
    # Chart data is passed to the `dataSource` parameter, as dict, in the form of key - value pairs.
    dataSource = OrderedDict()

    # The `mapConfig` dict contains key - value pairs data for chart attribute
    mapConfig = OrderedDict()
    mapConfig["caption"] = "Average Annual Population Growth"
    mapConfig["subcaption"] = "1955-2015"
    mapConfig["numbersuffix"] = "%"
    mapConfig["includevalueinlabels"] = "1"
    mapConfig["labelsepchar"] = ":"
    mapConfig["entityFillHoverColor"] = "#FFF9C4"
    mapConfig["theme"] = "fusion"

    # Map color range data
    colorDataObj = {
        "minvalue": "0",
        "code": "#FFE0B2",
        "gradient": "1",
        "color": [{
                "minValue": "0.5",
                "maxValue": "1",
                "code": "#FFD74D"
            },
            {
                "minValue": "1.0",
                "maxValue": "2.0",
                "code": "#FB8C00"
            },
            {
                "minValue": "2.0",
                "maxValue": "3.0",
                "code": "#E65100"
            }
        ]
    }

    dataSource["chart"] = mapConfig
    dataSource["colorrange"] = colorDataObj
    dataSource["data"] = []


    # Map data array
    mapDataArray = [
        ["NA", "0.82", "1"],
        ["SA", "2.04", "1"],
        ["AS", "1.78", "1"],
        ["EU", "0.40", "1"],
        ["AF", "2.58", "1"],
        ["AU", "1.30", "1"]
    ]


    # Iterate through the data in `mapDataArray` and insert in to the `dataSource["data"]` list.
    #The data for the `data` should be in an array wherein each element 
    #of the array is a JSON object# having the `id`, `value` and `showlabel` as keys.
    for i in range(len(mapDataArray)):
        dataSource["data"].append({
            "id": mapDataArray[i][0],
            "value": mapDataArray[i][1],
            "showLabel": mapDataArray[i][2]
        })

    # Create an object for the world map using the FusionCharts class constructor
    # The chart data is passed to the `dataSource` parameter.
    fusionMap = FusionCharts("maps/world", "myFirstMap", "650", "450", "myFirstmap-container", "json", dataSource)
    print(fusionMap)
    # returning complete JavaScript and HTML code, which is used to generate map in the browsers.
    return render(request, 'index.html', {'output2': fusionMap.render()
    })

def chart(request):
    # Create an object for the column2d chart using the FusionCharts class constructor

    #first arg : column chart => column2d, piechart=>pie2d,line =>line
    column2d = FusionCharts("line", "ex2" , "100%", "400", "chart-1", "json",
        # The data is passed as a string in the `dataSource` as parameter.
                        """{
                            "chart": {
                                "caption": "Recommended Portfolio Split",
                                "subCaption" : "For a net-worth of $1M",
                                "showValues":"1",
                                "showPercentInTooltip" : "0",
                                "numberPrefix" : "$",
                                "enableMultiSlicing":"1",
                                "theme": "fusion"
                            },
                            "data": [{
                                "label": "Equity",
                                "value": "300000"
                            }, {
                                "label": "Debt",
                                "value": "230000"
                            }, {
                                "label": "Bullion",
                                "value": "180000"
                            }, {
                                "label": "Real-estate",
                                "value": "270000"
                            }, {
                                "label": "Insurance",
                                "value": "20000"
                            }]
                           }""") 
    # returning complete JavaScript and HTML code, which is used to generate chart in the browsers.
    

    return render(request, 'index.html', {'output' : column2d.render()})
