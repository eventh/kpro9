@echo off
echo "Building LaTeX files"
if "%1" == "clean" goto clean
mkdir tmp
if "%1" == "" goto report
if "%1" == "all" goto all
if exist %1_standalone.tex goto standalone
echo "Unknown command %1"

:clean
    echo "Removing LaTeX build files"
    del /S *.aux *.toc *.log *.out *.lof *.lot
    rmdir /S /Q tmp
    goto :eof

:all
    for %%v in (plan prestudy requirements sprint1 sprint2 test) do (
        pdflatex -output-directory tmp %%v_standalone.tex
        pdflatex -output-directory tmp %%v_standalone.tex
        move /Y tmp\%%v_standalone.pdf %%v.pdf
    )
    goto :eof

:standalone
    pdflatex -output-directory tmp %1_standalone.tex
    pdflatex -output-directory tmp %1_standalone.tex
    move /Y tmp\%1_standalone.pdf %1.pdf
    start %1.pdf
    goto :eof

:report
    pdflatex -output-directory tmp report.tex
    pdflatex -output-directory tmp report.tex
    move /Y tmp\report.pdf report.pdf
    start report.pdf
    goto :eof
