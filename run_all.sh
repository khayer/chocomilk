for k in HF03-3 LP02-2 SC02-1 HF01-1 HF03-4 LP02-3 SC02-2 HF01-2 HF03-5 LP02-4 SC02-3 HF01-3 HF05-1 LP02-5 SC02-4 HF01-4 HF05-2 LP03-1 SC02-5 HF01-5 HF05-3 LP03-2 SC03-1 HF02-1 HF05-4 LP03-3 SC03-2 HF02-2 LP01-1 LP03-4 SC03-3 HF02-3 LP01-2 SC01-1 SC03-4 HF02-4 SC01-2 SC03-5 HF02-5 LP01-4 SC01-3 HF03-1 LP01-5 SC01-4 HF03-2 LP02-1 SC01-5 #LP01-3
do
    echo $k
    python plot_events.py ~/Dropbox/5c-MatDiet-SchA-Katherina/SCH-A-$k.csv > table.txt
    convert *.png $k.pdf
    mkdir ../$k
    cp $k.pdf ../$k
    mv table.txt ../$k
    mv $k.pdf /Users/hayer/Google\ Drive/Nicola/SC_control_animals/with_error_bars/
    rm *png
done
