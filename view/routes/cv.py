SKILLS = ["Flask", "Django", "numpy",
          "pandas", "SQLAlchemy", "scrapy", "matplotlib", "Requests", "nltk"]

@view.route("/send_cv", methods=['POST'])
def invite():
    post_data = request.get.json()
    matching_skills = set(SKILLS) & \
                      set(post_data['cv'])

    if len(matching_skills) >= 2:
       return jsonify({'invite': True})
    else:
        return jsonify({'invite': False})


if __name__ == "__main__":
    set_a = {1, 2, 3}
    set_b = {3, 4, 5}
    set_c = set_a.intersect(set_b)
    print(set_c)

