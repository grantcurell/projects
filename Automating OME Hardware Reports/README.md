# Automating OME Hardware Reports

## Tasks

- [x] Create a utility for running scans against OME
- [x] Figure out how to extract the hardware status specifically after the scan
- [ ] Figure out how to separate the servers that were recently added
- [ ] Figure out how if I need to force sync alerts
- [ ] Add the ability to remove servers from OME
  - [ ] (Optional) Determine if we want to put these in a discovery group?
- [ ] Create a utility for comparing the PCIe changes to a server between two hardware scans
  - [ ] First step is to be able to compare columns of a comma separated file
  - [x] Figure out how to pull the device hardware tab
- [ ] Create a lightweight API which allows Angular to query for data
  - [ ] Decide how to maintain data - JSON files? More complex option like MongoDB?
- [ ] Write a method for checking the hardware health on both scans
- [ ] Create an Angular project
  - [ ] Create functionality for running scan 1
  - [ ] Create functionality for running scan 2
  - [ ] Create functionality for outputting results
  - [ ] (Optional) Add text boxes for addition of additional columns/information
  - [ ] (Optional) Add a button for rechecking hardware health. Might be convienient?
- [ ] (Optional) Go back and fix exception handling for [Dell code](https://github.com/dell/OpenManage-Enterprise/tree/master/Core/Python)

## Missing Info

- We don't know where some of the fields are coming from. We assume customer

## Useful Links

- https://downloads.dell.com/manuals/all-products/esuprt_software/esuprt_ent_sys_mgmt/dell-openmanage-enterprise-v30_white-papers4_en-us.pdf
- https://www.dell.com/support/home/en-us/product-support/product/dell-openmanage-enterprise/docs
- https://topics-cdn.dell.com/pdf/poweredge-mx7000_api-guide5_en-us.pdf
- https://www.dell.com/support/manuals/us/en/04/dell-openmanage-enterprise-tech-release/lex_techrel_pub/groups-service?guid=guid-894c21ef-14f8-44ea-9e98-9e4e613ca4a3&lang=en-us

## For Jacob

1. Create a GitHub account if you don't already have one
2. [Download Gitkraken](https://www.gitkraken.com/download) and install it. Next, connect it to your GitHub account.
3. [Fork](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo) my [Dell repository](https://github.com/grantcurell/dell)
4. Use GitKraken to download your forked repository to your local machine
5. Open the folder "Automating OME Hardware Reports". All our code will be in the code folder and I have made a folder called "Jacob" for you to work in.
6. Use Excel to create two dummy files. They'll need a column header and the second should have some bogus data. Basically you just want to artificially recreate a scenario where you can find the delta between two columns that have the same name.
7. Use [this library](https://docs.python.org/3/library/csv.html) to read the CSV.
8. Using the column name, identify the two columns you want to compare in the two CSV files.
9. Output the delta between the two CSV files to a third CSV file
10. When you're finished making your code, [pull request](https://support.gitkraken.com/working-with-repositories/pull-requests/)] it to the master branch of my repository.