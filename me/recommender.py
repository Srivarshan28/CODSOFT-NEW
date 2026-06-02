import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
from tkinter import ttk, messagebox

data_games = {
    'Title': ['The Witcher 3', 'God of War Ragnarök', 'Black Myth: Wukong', 'Cyberpunk 2077', 'WWE 2K24'],
    'Tags': [
        'RPG fantasy open-world story-rich magic',
        'action adventure mythology narrative hack-and-slash',
        'action RPG mythology martial-arts difficult',
        'RPG sci-fi open-world futuristic shooter',
        'sports fighting simulation wrestling multiplayer'
    ]
}

# Movies Dataset
data_movies = {
    'Title': ['The Dark Knight', 'Inception', 'Interstellar', 'The Matrix', 'Avengers: Endgame'],
    'Tags': [
        'superhero action crime thriller batman joker',
        'sci-fi thriller mind-bending dream heist',
        'sci-fi space drama physics time-travel',
        'sci-fi action cyberpunk virtual-reality',
        'superhero action team-up marvel space'
    ]
}

# Comics Dataset
data_comics = {
    'Title': ['Watchmen', 'Batman: The Killing Joke', 'Spider-Man: Blue', 'Saga', 'The Sandman'],
    'Tags': [
        'superhero dark mystery graphic-novel psychological',
        'superhero batman joker dark psychological',
        'superhero romance marvel emotional',
        'sci-fi fantasy space-opera alien',
        'dark-fantasy mythology magic dream'
    ]
}

dfs = {
    'Games': pd.DataFrame(data_games),
    'Movies': pd.DataFrame(data_movies),
    'Comics': pd.DataFrame(data_comics)
}

similarities = {}
for category, df in dfs.items():
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['Tags'])
    similarities[category] = cosine_similarity(tfidf_matrix, tfidf_matrix)

def show_recommendations():
    """Runs the recommendation math based on the selected category and input."""
    category = category_var.get()
    user_choice = entry_item.get().strip()
    
    if not user_choice:
        messagebox.showwarning("Input Error", "Please enter a title.")
        return
        
    df = dfs[category]
    cosine_sim = similarities[category]
    
    match_mask = df['Title'].str.lower() == user_choice.lower()
    
    if not match_mask.any():
        available_items = "\n".join(df['Title'].tolist())
        messagebox.showerror("Not Found", f"'{user_choice}' is not in the {category} database.\n\nAvailable:\n{available_items}")
        return
        
    idx = df.index[match_mask].tolist()[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:3]  # Get top 2
    
    item_indices = [i[0] for i in sim_scores]
    recommendations = df['Title'].iloc[item_indices].tolist()
    
    result_text = f"🎯 Because you liked '{user_choice}':\n\n1. {recommendations[0]}\n2. {recommendations[1]}"
    label_result.config(text=result_text)

root = tk.Tk()
root.title("Media Recommender AI")
root.geometry("450x400") 
root.configure(padx=20, pady=20)

tk.Label(root, text="Media Recommendation Engine", font=("Helvetica", 16, "bold")).pack(pady=(0, 20))

tk.Label(root, text="1. Choose a Category:", font=("Helvetica", 10, "bold")).pack()
category_var = tk.StringVar()
category_dropdown = ttk.Combobox(root, textvariable=category_var, font=("Helvetica", 12), state="readonly")
category_dropdown['values'] = ('Games', 'Movies', 'Comics')
category_dropdown.current(0) # Set default to Games
category_dropdown.pack(pady=10)

tk.Label(root, text="2. Enter a title you like:", font=("Helvetica", 10, "bold")).pack(pady=(15, 0))
entry_item = tk.Entry(root, font=("Helvetica", 14), width=25, justify="center")
entry_item.pack(pady=10)

btn_recommend = tk.Button(root, text="Get Recommendations", font=("Helvetica", 12, "bold"), 
                          bg="#4CAF50", fg="white", command=show_recommendations)
btn_recommend.pack(pady=20)

label_result = tk.Label(root, text="", font=("Helvetica", 13), fg="#333333", justify="left")
label_result.pack(pady=10)

root.mainloop()