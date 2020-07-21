# Automating OME Hardware Reports

## Tasks

- [ ] Create a utility for comparing the PCIe changes to a server between two hardware scans
  - [ ] First step is to be able to compare columns of a comma separated file
- [ ] Create a lightweight API which allows Angular to query for data
  - [ ] Decide how to maintain data - JSON files? More complex option like MongoDB?
- [ ] Create an Angular project
  - [ ] Create functionality for running scan 1
  - [ ] Create functionality for running scan 2
  - [ ] Create functionality for outputting results
  - [ ] (Optional) Add text boxes for addition of additional columns/information

## For Jacob

1. Create a GitHub account if you don't already have one
2. [Fork](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo) my [Dell repository](https://github.com/grantcurell/dell)
3. Open the folder "Automating OME Hardware Reports". All our code will be in the code folder and I have made a folder called "Jacob" for you to work in.
4. Use Excel to create two dummy files. They'll need a column header and the second should have some bogus data. Basically you just want to artificially recreate a scenario where you can find the delta between two columns that have the same name.
5. Use [this library](https://docs.python.org/3/library/csv.html) to read the CSV.
6. Using the column name, identify the two columns you want to compare in the two CSV files.
7. Output the delta between the two CSV files to a third CSV file