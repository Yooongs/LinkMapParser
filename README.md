# LinkMapParser
parsing ios linkmap file and compare two linkmap file:add,delete,size change.

## what can do?

1. parsing one linkmap, get size of Different Object files
2. compare two linkmap, you can know size change and file add or delete

## what u need?

1. python 2.7
2. link map file

## Usage

### parsing one linkmap file

```
python parselinkmap.py ${linkmap_path}.txt
```

then you need intput unit, mb or kb.
you can get result link this:

```
python parselinkmap.py /Users/${user}/Desktop/linkmap/ddemo.txt /Users/${user}/Desktop/linkmap/ddemo2.txt
intput unit(mb/kb):kb
================================================================================
            /Users/${user}/linkmap/ddemo.txt each size of Object files           
================================================================================
Creating Result File : /Users/${user}/Desktop/linkmap/BaseLinkMapResult.txt
AppDelegate.o                                     13.0000kb
ViewController.o                                  9.6406kb
SceneDelegate.o                                   4.6357kb
UIWebViewController.o                             2.4824kb
main.o                                            0.1934kb
total size:                                       29.9521kb

```

### parsing two linkmap file, and compare

```
python parselinkmap.py ${linkmap_baseline_path}.txt ${linkmap_target_path}.txt
```
also, you need input unit
intput unit(mb/kb):kb

```
 python parselinkmap.py /Users/${user}/Desktop/linkmap/ddemo.txt /Users/${user}/Desktop/linkmap/ddemo2.txt
intput unit(mb/kb):kb
================================================================================
            /Users/${user}/Desktop/linkmap/ddemo.txt each size of Object files           
================================================================================
Creating Result File : /Users/${user}/Desktop/linkmap/BaseLinkMapResult.txt
AppDelegate.o                                     13.0000kb
ViewController.o                                  9.6406kb
SceneDelegate.o                                   4.6357kb
UIWebViewController.o                             2.4824kb
main.o                                            0.1934kb
total size:                                       29.9521kb


================================================================================
           /Users/${user}/Desktop/linkmap/ddemo2.txt each size of Object files           
================================================================================
Creating Result File : /Users/${user}/Desktop/linkmap/TargetLinkMapResult.txt
AppDelegate.o                                     13.0000kb
ViewController.o                                  12.5957kb
SceneDelegate.o                                   4.6357kb
ADDTest1.o                                        0.2354kb
ADDTest.o                                         0.2344kb
main.o                                            0.1934kb
total size:                                       30.8945kb


================================================================================
                                   compare result                                   
================================================================================
Object files                                          base line     target        add+/delete-  
ViewController.o                                      9.6406kb      12.5957kb     2.9551
ADDTest1.o                                            0.0000kb      0.2354kb           +      
ADDTest.o                                             0.0000kb      0.2344kb           +      
UIWebViewController.o                                 2.4824kb      0.0000kb           -     
```

**Reference**: https://github.com/zgzczzw/LinkMapParser
