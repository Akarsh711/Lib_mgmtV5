







def bookid_finder(arr):
    var = 'chemistry' #value in place of request.form.get()
    x = 0
    for i in arr:
        for j in i:
            if var==j:
                x = i[0]
                return x

#json_converter function is used to convert json params to list of tuples
def json_converter(j_son):
    y = dict(j_son)

    #this thing idk, but convert dictionary in list
    x =[(key, values) for key, values in y.items()]

    #creating list from dictionary
    z=[]
    for i in range(len(x)):
        for j in range(0,2):
            t=x[i][j]#it's same as x[i][j]
            t = str(t)
            q = t.split(",")
            z.append(q)
    return z

#finding value in list
def key_finder(z, value):
    value = str(value)
    prev_i=0
    for i in z:
        val = 'math'
        for j in i:
            if j == value:
                return prev_i
                break
        prev_i = i
    

'''z = json_converter(p["books_ids"])  '''
#y = key_finder(z, 'chemistry 1')
#print("wola we get value from function", y)

'''@app.route("/")
def test_route():
    return render_template("test.html")

@app.route("/response", methods=['POST','GET'])
def response():
    book_name = request.form.get("name")
    book_id = request.form.get("id")
    
    bookId_string = ""
    count = 0
    j = 0

    for i in book_name.split(","):
        count = count + 1

    count = count - 1
    for i in book_name.split(","):
        y = key_finder(z, i)
        
        if j < count:
            bookId_string = bookId_string + y[0] + ","
        else:
            bookId_string = bookId_string + y[0] 
        j = j+1

    return render_template("test2.html", data = bookId_string)

var = [['0101'],['0102']]
var = str(var)
print("var is something = ",var)

app.run(debug=True)'''