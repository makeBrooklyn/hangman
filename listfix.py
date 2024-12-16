def main():
   with open('words.txt', 'r') as file:
      words = [word.strip().lower() for word in file]

   filtered_words = []
   for word in words:
      if 6 <= len(word) <= 12:
         filtered_words.append(word)

   # write the filtered list back to a new file
   with open('filtered_words.txt', 'w') as file:
      for word in filtered_words:
         file.write(word + '\n')
         print(word)

if __name__ == "__main__":
    main()