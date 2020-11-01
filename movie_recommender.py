import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


#these are the helping functions
def get_title_from_index(index):
	return df[df.index == index]["title"].values[0]

def get_index_from_title(title):
	return df[df.title == title]["index"].values[0]
##################################################

##Step 1: Read CSV File
df=pd.read_csv("movie_dataset.csv")

##Step 2: Select Features
features=['keywords','cast','genres','director']

##Step 3: Create a column in DF which combines all selected features
for feature in features:
	df[feature]=df[feature].fillna(" ")

def combine_features(row):
	try:
		return row['keywords'] +"  "+row['cast']+"  "+row['genres']+"  "+row['director']
	except:
		print("error",row)

df["combined_features"]=df.apply(combine_features,axis=1)


##Step 4: Create count matrix from this new combined column
cv=CountVectorizer()

count_matrix=cv.fit_transform(df["combined_features"])

##Step 5: Compute the Cosine Similarity based on the count_matrix
cosine_sim=cosine_similarity(count_matrix)


''''----------------------------------------gui------------------------------------------------------'''


from tkinter import *
from PIL import Image,ImageTk
root=Tk()

HEIGHT=480
WIDTH=640
canvas=Canvas(root,height=HEIGHT,width=WIDTH)
canvas.pack()
root.title("Movie_Recomedation_System")

def test_function(entry):

	movie_user_likes=entry
	lowerframe.delete(0.0,END)

	## Step 6: Get index of this movie from its title
	try:
		movie_index = get_index_from_title(movie_user_likes)

		similar_movies = list(enumerate(cosine_sim[movie_index]))

		##step-7:Get the list of similar movies in Descending order of simliarity score

		sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)

	except Exception:
		msg="\n\n\n\nSorry,We Couldnot  Find The Movie You Requested"
		lowerframe.insert(END,msg)


#printing the similar movies on to the gui window:

	i=0
	j=0
	List=[None]*10
	for element in sorted_similar_movies:
		s = get_title_from_index(element[0])
		List[j] = s
		j = j + 1
		i = i + 1
		if i >= 10:
			break


	for x in range(len(List) - 1, -1, -1):
		t = "\n"
		lowerframe.insert(0.0, List[x])
		lowerframe.insert(0.0, t)

#adding image to gui background
img=ImageTk.PhotoImage(Image.open("1.jpg"))
label=Label(image=img).place(x=0,y=0,relwidth=1,relheight=1)

#creation of frame to hold the entry feild and search button
frame=Frame(root,bg="#ff704d",bd=5)
frame.place(relx=0.5,rely=0.1,relwidth=0.75,relheight=0.1,anchor="n")

#creating entry feild for user to enter movie name

entry=Entry(frame,font=40)
entry.place(relwidth=0.65,relheight=1)


# creating search button
button=Button(frame,text="search",font=40,activebackground="#ffff4d",relief="raised",bg="#404040",fg="white",command=lambda:test_function(entry.get()))
button.place(relx=0.7,relwidth=0.3,relheight=1)

#creating the text window to display all the similar movies
lowerframe=Text(root,bg="white",bd=10,font=200,relief="sunken")
lowerframe.place(relx=0.5,rely=0.25,relwidth=0.75,relheight=0.6,anchor="n")

label=Label(lowerframe,text="Top 10 Recommnedations",bg="white",font=20).pack()

root.mainloop()


