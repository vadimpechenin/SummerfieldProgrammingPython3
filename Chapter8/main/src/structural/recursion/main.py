def indented_list_sort(indented_list, indent="    "):
   """Returns an alphabetically sorted copy of the given list

   The indented list is assumed to be a list of strings in a
   hierarchy with indentation used to indicate child items.
   The indent parameter specifies the characters that constitute
   one level of indent.

   The function copies the list, and returns it sorted in
   case-insensitive alphabetical order, with child items sorted
   underneath their parent items, and so on with grandchild items,
   and so on recursively to any level of depth.

   >>> indented_list = ["M", " MX", " MG", "D", " DA", " DF",\
   "  DFX", "  DFK", "  DFB", " DC", "K", "X", "H", " HJ",\
   " HB", "A"]
   >>>
   >>> indented_list = indented_list_sort(indented_list, " ")
   >>> indented_list[:8]
   ['A', 'D', ' DA', ' DC', ' DF', '  DFB', '  DFK', '  DFX']
   >>> indented_list[8:]
   ['H', ' HB', ' HJ', 'K', 'M', ' MG', ' MX', 'X']
   """
   KEY, ITEM, CHILDREN = range(3)

   def add_entry(level, key, item, children):
      if level == 0:
         children.append((key, item, []))
      else:
         add_entry(level - 1, key, item, children[-1][CHILDREN])

   def update_indented_list(entry):
      indented_list.append(entry[ITEM])
      for subentry in sorted(entry[CHILDREN]):
         update_indented_list(subentry)

   entries = []
   for item in indented_list:
      level = 0
      i = 0
      while item.startswith(indent, i):
         i += len(indent)
         level += 1
      key = item.strip().lower()
      add_entry(level, key, item, entries)

   indented_list = []
   for entry in sorted(entries):
      update_indented_list(entry)
   return indented_list


def indented_list_sort_local(indented_list, indent="    "):
   """
   Given an indented list, i.e., a list of items with indented
   subitems, sorts the items, and the subitems within each item (and so
   on recursively) in case-insensitive alphabetical order.

   >>> indented_list = ["M", " MX", " MG", "D", " DA", " DF", "  DFX", \
   "  DFK", "  DFB", " DC", "K", "X", "H", " HJ", " HB", "A"]
   >>>
   >>> indented_list = indented_list_sort_local(indented_list, " ")
   >>> indented_list[:8]
   ['A', 'D', ' DA', ' DC', ' DF', '  DFB', '  DFK', '  DFX']
   >>> indented_list[8:]
   ['H', ' HB', ' HJ', 'K', 'M', ' MG', ' MX', 'X']
   """
   KEY, ITEM, CHILDREN = range(3)

   def add_entry(key, item, children):
      nonlocal level
      if level == 0:
         children.append((key, item, []))
      else:
         level -= 1
         add_entry(key, item, children[-1][CHILDREN])

   def update_indented_list(entry):
      indented_list.append(entry[ITEM])
      for subentry in sorted(entry[CHILDREN]):
         update_indented_list(subentry)

   entries = []
   for item in indented_list:
      level = 0
      i = 0
      while item.startswith(indent, i):
         i += len(indent)
         level += 1
      key = item.strip().lower()
      add_entry(key, item, entries)

   indented_list = []
   for entry in sorted(entries):
      update_indented_list(entry)
   return indented_list

def factorial(x):
   if x <=1:
      return 1
   return x * factorial(x-1)

def main():
   #Факториал
   x = 10
   result = factorial(x)
   print("Факториал {0}: ".format(x) + str(result))

if __name__ == '__main__':
   main()