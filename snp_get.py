import re
import os
import argparse
parser = argparse.ArgumentParser(description='Author:Peng Zhao <pengzhao@nwafu.edu.cn>')
parser.add_argument('-gene', type=str)
parser.add_argument('-vcf', type=str)
parser.add_argument('-length', type=str)
parser.add_argument('-out', type=str)
args = parser.parse_args()
inf_name = args.gene
vcf_name = args.vcf
length = args.length
ouf_prefix = args.out
mk_dir = "mkdir ./temp/"
os.system(mk_dir)
inf = open(inf_name,"r")
ouf = open("./temp/gene.bed","w")
for line in inf:
    line = line.replace("\n","")
    li = re.split("\t",line)
    pos1 = int(li[1]) - 1 - int(length)
    pos2 = int(li[2]) + int(length)
    if pos1 >= 0:
        ouf.write("%s\t%s\t%s\t%s\n" % (li[0],pos1,pos2,li[3]))
    else:
        ouf.write("%s\t%s\t%s\t%s\n" % (li[0],"0",pos2,li[3]))
ouf.close()
inf2 = open(vcf_name,"r")
ouf2 = open("./temp/vcf.bed","w")
for line2 in inf2:
    line2 = line2.replace("\n","")
    li2 = re.split("\t",line2)
    if li2[0][:1] != "#":
        pos3 = int(li2[1]) - 1
        snp_id = str(li2[0]) + "&" + str(li2[1])
        ouf2.write("%s\t%s\t%s\t%s\n" % (li2[0],pos3,li2[1],snp_id))
ouf2.close()
bed_command = "bedtools intersect -a ./temp/vcf.bed -b ./temp/gene.bed -wa -wb | bedtools groupby -i - -g 1-4 -c 8 -o collapse > ./temp/overlap.out"
os.system(bed_command)
overlap_gene = str(ouf_prefix) + ".snp.gene.out"
inf3 = open("./temp/overlap.out","r")
ouf3 = open(overlap_gene,"w")
for line3 in inf3:
    line3 = line3.replace("\n","")
    li3 = re.split("\t",line3)
    if li3[4] != ".":
        ouf3.write("%s\t%s\n" % (li3[3],li3[4]))
ouf3.close()
ouf_vcf = str(ouf_prefix) + ".snp.gene.vcf"
inf4 = open(overlap_gene,"r")
inf5 = open(vcf_name,"r")
ouf4 = open(ouf_vcf,"w")
dict_snp = {}
for line4 in inf4:
    line4 = line4.replace("\n","")
    li4 = re.split("\t",line4)
    dict_snp[li4[0]] = "1"
for line5 in inf5:
    line5 = line5.replace("\n","")
    li5 = re.split("\t",line5)
    if li5[0][:1] != "#":
        snp_id2 = str(li5[0]) + "&" + str(li5[1])
        if snp_id2 in dict_snp:
            ouf4.write("%s\n" % (line5))
    else:
        ouf4.write("%s\n" % (line5))
rm_command = "rm -r ./temp"
os.system(rm_command)
print("DONE")
