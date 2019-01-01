/*
* Imagej plugin to read Nikon STORM bin file.
* Displays INI information, starting from [InsightH] section
*/

import ij.*;
import ij.process.*;
import ij.gui.*;
import java.awt.*;
import ij.plugin.*;
import ij.plugin.frame.*;
import ij.io.*;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;


public class Read_Storm_bin implements PlugIn {
        
        byte[] data;

	public void run(String arg) {
                try {
                        OpenDialog odlg = new OpenDialog("select a bin");
                        File inputFile = new File(odlg.getPath());
                        data = new byte[(int)inputFile.length()];
                        //IJ.log(""+data.length);
                        FileInputStream fis = new FileInputStream(inputFile);
                        fis.read(data, 0, data.length);
                        String contents = new String(data);
                        int pos0 = contents.indexOf("[InsightH]");
                        int pos1 = contents.indexOf("V1META");
                        if(pos0 == -1)IJ.log("did not find [InsightH]");
                        if(pos1 == -1)IJ.log("did not find V1META");
                        IJ.log(contents.substring(pos0,pos1));
                        fis.close();
                }catch(FileNotFoundException ex)
                {}catch (IOException ex) {}
	}

}
