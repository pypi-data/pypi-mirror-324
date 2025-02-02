import csv

def add(a, b):
    """Returns the sum of two numbers"""
    return a + b

def parse_file(file_name):
    """Parses a tab-separated values file (tsv). Ignores empty lines and those that start with '#'. See scripts/courses/tci.txt for example file layout."""

    with open(file_name, "r", newline='', encoding="utf-8") as file:
        reader = csv.reader(file, delimiter="\t")

        # slurp in all lines from the file, skipping those that start with # and those that are empty
        data = [row for row in reader if row and not row[0].startswith("#")]

## copied from https://course.bluegolf.com/bluegolf/course/course/tcofiowa/detailedscorecard.htm
# Click the dropdown at top left of scorecard and select "SHOW ALL"
# 
# TEE	1	2	3	4	5	6	7	8	9	OUT	10	11	12	13	14	15	16	17	18	IN	TOT
# KING	392	415	186	593	185	480	556	456	156	3419	427	376	442	515	325	194	222	637	456	3594	7013
# MASTER	341	386	175	578	180	467	548	396	151	3222	356	344	427	476	310	175	191	596	434	3309	6531
# PALMER	328	368	157	544	161	440	523	385	145	3051	322	328	379	440	258	154	164	554	390	2989	6040
# DEACON	300	314	139	513	141	414	500	341	136	2798	311	301	343	430	229	147	150	520	338	2769	5567
# LEGEND	243	258	105	470	102	376	419	296	115	2384	262	283	298	334	223	85	110	512	331	2438	4822
# LEGEND (FORWARD)	243	258	105	470	102	376	419	296	115	2384	262	283	298	334	131	85	110	512	331	2346	4730
