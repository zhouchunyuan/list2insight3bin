macro "Unused Tool- 1" {}
macro "STORM list Action Tool -  CcccD55D57D5aD66D6aD7bD81D85D8aD93Da6DadDbdDc6Dd6C333Db1Dc2Dd3CeeeD34D35D4cD69D77Dc9Dd9CdddD32D33D42D43D47D52D53D59D63D64D73D7aD87D89D97D99D9bDa9Db9DcaDd8CbbbD58D75D7dD8bD96D9dDa4CfffD00D01D02D03D04D05D06D07D08D09D0aD0bD0cD0dD0eD0fD10D11D12D13D14D15D16D17D18D19D1aD1bD1cD1dD1eD1fD20D21D22D23D24D25D26D27D28D29D2aD2bD2cD2dD2eD2fD30D3bD3cD3dD3eD40D4eD50D5eD60D6eD70D7eD80D8eD90D9eDa0DaeDb0DbeDc0Dc1DceDd0Dd1Dd2De0De1De2De3De4De5De6De7De8De9DeaDebDecDedDeeDefDf0Df1Df2Df3Df4Df5Df6Df7Df8Df9DfaDfbDfcDfdDfeDffCdddD31D41D44D4aD4bD51D54D5bD62D67D72D74D83D84D8dDa7Db2Db7Dc7DcbDcdDd7CaaaD95Db5CfffD38D39D3aD6cD7cD8cDb3DbcDccDdbDdcDddDdeCbbbD45D5dD68D6bD78D88D92D9aDaaDabDb4Db8DbbDc8CcccD46D48D4dD56D61D6dD71D76D82D86D94Da1Da2Da3DbaDc3Dc4Dd4C777D3fD4fD5fD6fD7fD8fD9fDafDbfDcfDdfCeeeD36D37D49D5cD79D9cDacDdaCaaaD65D91D98Da5Da8Db6Dc5Dd5"{

	requires("1.52");

	pixelSize = 160;//nm

	html = "<html>"
		+"<h2>Insight3 List To N-STORM Tool 1.0</h2>"
		+"<b>Usage:</b><br>"
		+"Select camera type in popup dialog.<br>"
		+"Choose the N-STORM molecule list.<br>"
		+"<font color=red>It takes some time to open the list file.</font>(typically 30 seconds)<br>"
		+"During the procedure, there will be messages in the status bar ...<br>"
		+"A 'save as' dialog will pop up when finishing converting.<br>"
		+"Then, please save it using a prefered file name.<br>"
		+"<br>An imageJ macro written by : Chunyuan Zhou<br>"
		+"Dec. 28, 2018<br>";

	Dialog.create("Select Pixel Size");
	Dialog.addHelp(html);
	Dialog.addChoice("Type:", newArray("160 nm ( EMCCD )", "162.5 nm ( sCMOS )"));
	Dialog.show();

	pixelSizeInfo = Dialog.getChoice();

	// default to EMCCD 160 nm
	// sCMOS pixel size = 65 nm. But with 0.4x zoom
	// the final pixel size becomes 162.5
	if(pixelSizeInfo == "162.5 nm ( sCMOS )")pixelSize = 162.5 ;

	showStatus("Openning molecule list, please wait ...");
	path = File.openDialog("Select STORM list:txt");
	Table.open(path);

	Table.showRowNumbers(0);
	columnNames = split(Table.headings(),"\t");

	showStatus("get channel index string");
	chNames = Table.getColumn(columnNames[0]);
	chNamesStr = "Z Rejected";
	for(i=0;i<Table.size;i++){
		if( indexOf(chNamesStr,chNames[i])<0 ) 
			chNamesStr += "\t"+chNames[i];
	}

	showStatus("change channel names into numbers");
	chNameArray = split(chNamesStr,"\t");
	for(i=0;i<Table.size;i++){
		for(j=0;j<chNameArray.length;j++){
			if( chNames[i] == chNameArray[j] ){
				Table.set(columnNames[0], i, j);
			}
		}
		showProgress(i, Table.size);
	}

	showStatus("scale down to camera pixel size based coordinates"); 
	for(i=0;i<Table.size;i++){
		x = Table.get("X",i)/pixelSize;
		xc = Table.get("Xc",i)/pixelSize;
		y = Table.get("Y",i)/pixelSize;
		yc = Table.get("Yc",i)/pixelSize;

		Table.set("X", i, x);
		Table.set("Xc", i, xc);
		Table.set("Y", i, y);
		Table.set("Yc", i, yc);	

		showProgress(i, Table.size);
	}

	showStatus("delete useless columns");
	for(i=18;i<columnNames.length;i++){
		Table.deleteColumn(columnNames[i]); 
	}

	//change channel name to Cas####
	Table.renameColumn(columnNames[0], "Cas"+Table.size);
	columnNames[0]= "Cas"+Table.size;

	Table.update();

	showStatus("saving list as txt");

	while(1){
		outputFile = File.openDialog("Save as ...");
		if(File.exists(outputFile)){
			if(getBoolean("File exists. Overwrite?")){
				break;
			}
		}else{
			break;
		}
	}

	Table.save(outputFile);

	Dialog.create("Process finished.");
	Dialog.addMessage("New List Saved: "+outputFile);
	Dialog.show();
}
