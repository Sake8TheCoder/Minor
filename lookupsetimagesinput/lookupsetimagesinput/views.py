from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
from .ImageDetection import process_image

from .WikiLinks import generate_wikipedia_links

def LookUp(request,context,k):
  n = len(context["Images"])
  uniqueLabels = {}
  for img in context["Images"]:
    processed = process_image(img)
    for item in processed:
      if item[0] not in uniqueLabels:
        uniqueLabels[item[0]] = []
      uniqueLabels[item[0]].append(item[1])

  sortedList = []
  for key in uniqueLabels:
    entry = [sum(uniqueLabels[key])/n, key]
    sortedList.append(entry)


  sortedList = sorted(sortedList,reverse=True)
  sortedList = sortedList[0:k]
  objects = {}
  for obj in sortedList:
      label = obj[1]
      objects[label] = []
      #generate wiki links with label
      wikiLinks = generate_wikipedia_links(label)
      #pair each link with amazon link
      for link in wikiLinks:
        item = link[30:]
        pair = [link,f"https://www.amazon.com/s?k={item}"]
        objects[label].append(pair)
  return render(request,"LookUp.html",{'objects':objects})

def indexPage(request):

  if request.method == "POST":
    file1 = request.FILES.get("Image1")
    file2 = request.FILES.get("Image2")
    file3 = request.FILES.get("Image3")
    file4 = request.FILES.get("Image4")
    allFiles = [file1,file2,file3,file4]
    if not file1 and not file2 and not file3 and not file4:
        messages.info(request,"No file has been entered")
        return redirect(indexPage)
    Imgs = {"Images" : []}
    for file in allFiles:
      if not file:
        continue

      extension = file.name.lower().rsplit('.', 1)[-1]
      if extension not in {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp'}:
        messages.info(request,"Enter image file extensions only")
        return redirect(indexPage)
      
      Imgs["Images"].append(file)

    return LookUp(request,Imgs,3)
  
  return render(request,"index.html")


  

