~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~
Dissertation Guidelines 
~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~
Version 4.5
Date: 07 October 2016
Address: CVR Lab, Department of CSE, NIT Rourkela, 769008, Odisha, India.
http://nitrkl.ac.in
~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~
===Description===
It has a LaTeX template to write dissertation 
for any academic degree at National Institute of Technology Rourkela.
~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~
===File Organization===
Download the zipped file from (Academic -> Dissertation Template)
	at the URL http://nitris.nitrkl.ac.in 
	
Unzip and store in any folder of your convenience; 
you will find the following files/folder in it ---
.	NITRdissertationTemplateV4_5
		DissertationGuidelinesV4_5.tex
		FrontPages.tex
		NITR.cls
		README.txt
		DissertationGuidelinesV4_5.pdf
.		Chap00
			Dedication.tex
			Acknowledge.tex
			Abstract.tex
			NITlogo.eps
.		Chap01
			Guidelines.tex
.		Chap02
			Unstructured.tex
.		Chap03
			Conclusion.tex
.		Ref
			SampleReferences.bib
			IEEEtran.bst
			asme.bst
			achemso.bst
			bmes.bst
			naturemag.bst
			osajnl.bst
			rsc.bst
			SampleDissemination.tex
			
Read the pdf file "DissertationGuidelinesV4_5.pdf" for a detailed guidelines.
~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~
===Use of MikTeX/TeXLive===
Use latest MikTeX or TeXLive as some features of the template may not be compatible with older versions. 
MiKTeX 2.9.5840 can be downloaded from Academic -> Dissertation Template at NITRIS. 
Uninstall the older version of MikTeX from your computer and install the latest version.
~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~
===How to use it===
(1) Enter your details in file "FrontPages.tex".
(2) Write your chapters and put in appropriate folders.
(3) Call each file from "DissertationGuidelinesV4_5.tex"
(4) You can add as many folders you require.
(5) If you use command prompt the use the following four commands
		>xelatex DissertationGuidelinesV4_5.tex
		>bibtex DissertationGuidelinesV4_5
		>xelatex DissertationGuidelinesV4_5.tex
		>xelatex DissertationGuidelinesV4_5.tex
   If you prefer to use any integrated development environment (IDE) like TexStudio, LEd etc
   then press appropriate button that would execute xelatex command.
(6) Your pdf file is now ready.
(7) Print it 
	(a) by setting A4 paper in printer properties
	and
	(b) by selecting the "Actual Size" in "Page Sizing & Handling"
~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~