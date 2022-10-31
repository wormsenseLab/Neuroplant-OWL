import PySimpleGUI as sg
import analyze_image as ai
import pathlib as plb
import unblind_key as un
import tkinter as tk
import dataviz as dv
import timepoint_add as tl
import colors_key as ck
import webbrowser

#import connect_metadata as cm
sg.ChangeLookAndFeel('GreenTan')

### Generates the first window that the user encounters.
### Opens upon running the program
def make_win1():
    layout1 = [
    [sg.Text('Welcome to Our Worm Locator!', size=(60, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
    [sg.Frame(layout=[[sg.Text('Click on the button below to access the image analysis functionalities of the OWL', font=(14))], [sg.Button('Analyze images', key='_IMG_ANALYSIS_', enable_events=True, font=(14))]], title='Image analysis',title_color='black', relief=sg.RELIEF_SUNKEN)],
    [sg.Text('_'  * 120)],
    [sg.Text('Would you like to perform data visualization?', font=(14))],
    [sg.Frame(layout=[[sg.Radio('Yes, two group estimation plot', 'RADIO1', default=False, size=(50,1), key='_DataVizTwoGroup_', enable_events=True, font=(14))], [sg.Radio('Yes,  shared control estimation plot', 'RADIO1', key='_DataVizSharedControl_', enable_events=True, font=(14))], [sg.Radio('Yes, multi 2 group estimation plot', 'RADIO1', key='_DataVizMultiTwo_', enable_events=True, font=(14))]], title='Options',title_color='black', relief=sg.RELIEF_SUNKEN)],
    [sg.Text('_'  * 120)],
     [sg.Text('Would you like to unblind your metadata sheet or your batch results file?',size=(80,1), font='Lucida', justification='left')], [sg.Radio('Yes', 'RADIO1', default=False, key='_Yes_', enable_events=True, font=(14))],
    [sg.Text('_'  * 120)],
    [sg.Text('If you have timelapse scans, would you like to add time points collumn to your batch results file?',size=(100,1), font='Lucida', justification='left')], [sg.Radio('Yes', 'RADIO1', default=False, key='_TimeLapseCollumn_', enable_events=True, font=(14))]
    , [sg.Exit()]]

    window1 = sg.Window('Worm Counter', layout1, default_element_size=(60, 2), resizable=True, finalize=True)
    return window1

### Makes the window to process multiple images

text_style = {
    'size': (40, 1),
    'justification': 'right'
}
box_style = {
    'size': (25, 1)
}

RM_URL = 'https://github.com/wormsenseLab/Neuroplant-OWL'
MD_URL = 'https://docs.google.com/spreadsheets/d/1u8PN5a5s7SFurxspXNJSq5FKKNKTdzFmCgwjjsEf4XE/edit?usp=sharing'
ttip = 'Link to Metadata template'


def make_batch_win():

    ia_inupt_column = [
    [sg.Text('Folder containing images to analyze: ',  **text_style),sg.In(**box_style, enable_events=True, key='-image_folder-',), sg.FolderBrowse()],
    [sg.Text('Metadata file (Optional): ', **text_style), sg.In(**box_style, key = 'md_file'), sg.FileBrowse(),],
    [sg.Text('Select a folder to store your results: ', **text_style),sg.In(**box_style, key = '-results_folder-'), sg.FolderBrowse()],
    [sg.Text('Name your summary file: ', **text_style),
    sg.In( **box_style, key='-name-') ],
    [sg.Button('Analyze'), sg.Button('Back'), sg.Exit()]]

    ia_text_column = [
    [sg.Text('1. The OWL will process ALL images contained in a single folder.')],
    [sg.Text('2. Inputing a metadata sheet will allow you to connect experimental\nconditions to the corresponding wells of an image.')],
    [sg.Text('Link to download the accepted Metadata Template', key='_mdTemplate_', tooltip=ttip, enable_events=True, text_color='blue')],
    [sg.Text('3. The OWL will return the results as .csv files to the folder specified.')],
    [sg.Text('4. The returned results will include multiple files containing the location\ndata for each well and a summary file.')],
    [sg.Text('Link to Documentation', key='_README_', tooltip=RM_URL, enable_events=True, text_color='blue'),]
    ]



    layout2 = [
    [sg.Column(ia_text_column),
    sg.VSeperator(),
    sg.Column(ia_inupt_column),]
    ]

    batch_window = sg.Window('OWL', layout2, default_element_size=(80, 1), resizable=True, finalize=True)
    return batch_window


### Creates the GUI window to process one image at a time
# def make_single_win():
#     layout3 = [
#     [sg.Frame('Single Pic', key = '_test_', font=(14), layout=[

#     [sg.Frame('Worm Strains in Each Well', visible = False, key='-4Strains-', font=(14),layout=[
#     [sg.Text('Strain in Well A', size=(15,1), font=(12)), sg.InputText(key='-StrainA-')],
#     [sg.Text('Strain in Well B', size=(15,1), font=(12)), sg.InputText(key='-StrainB-')],
#     [sg.Text('Strain in Well C', size=(15,1), font=(12)), sg.InputText(key='-StrainC-')],
#     [sg.Text('Strain in Well D', size=(15,1), font=(12)), sg.InputText(key='-StrainD-')]])],

#     [sg.Frame('Slot 1 Data', visible = True, font=(14), layout=[
#     #[sg.Checkbox('Check this box if you there are multiple strains on this plate', enable_events=True ,key='-show_strains-', size=(10,1))],
#     [sg.Text('Plate ID', size=(15,1), font=(12)), sg.InputText(key='-PID1-')],
#     [sg.Text('Strain on Plate 1', size=(15,1), font=(12)), sg.InputText(key='-Strain1-')],
#     [sg.Text('Compound', size=(15,1), font=(12)), sg.InputText(key='-Compound1-')]]
#     ),
#     sg.Frame('Slot 2 Data',visible = True, font=(12), layout=[
#     [sg.Text('Plate ID', size=(15,1), font=(12)), sg.InputText(key='-PID2-')],
#     [sg.Text('Strain on Plate 2', size=(15,1), font=(12)), sg.InputText(key='-Strain2-')],
#     [sg.Text('Compound', size=(15,1), font=(12)), sg.InputText(key='-Compound2-')]
#     ])],

#     [sg.Frame('Slot 3 Data',visible = True, font=(14), layout=[
#     [sg.Text('Plate ID', size=(15,1), font=(12)), sg.InputText(key='-PID3-')],
#     [sg.Text('Strain on Plate 3', size=(15,1), font=(12)), sg.InputText(key='-Strain3-')],
#     [sg.Text('Compound', size=(15,1), font=(12)), sg.InputText(key='-Compound3-')]]
#     ),
#     sg.Frame('Slot 4 Data',visible = True,  font=(14), layout=[
#     [sg.Text('Plate ID', size=(15,1), font=(12)), sg.InputText(key='-PID4-')],
#     [sg.Text('Strain on Plate 4', size=(15,1), font=(12)), sg.InputText(key='-Strain4-')],
#     [sg.Text('Compound', size=(15,1), font=(12)), sg.InputText(key='-Compound4-')]
#     ])],

#     [sg.Frame('Choose the image file to be analyzed', visible=True, font=(12),layout=[
#     [sg.Text('Choose a folder to save your results in: ', size=(40, 1), auto_size_text=False, font=(12), justification='right'),
#         sg.InputText('Results folder', key='-results-'), sg.FolderBrowse()],
#     [sg.Text('Select the image to be analyzed', size=(40, 1), auto_size_text=False, font=(12), justification='right'), sg.InputText('Image file', key='-file-'), sg.FileBrowse()],
#         [sg.Button('Analyze'), sg.Button('Back'), sg.Exit()]])]
#     ])]]

#     single_im = sg.Window('Single Image Processing', layout3, default_element_size=(80, 1), resizable=True, finalize=True)
#     return single_im
 

def unblind_window():
    layout4 = [
    [sg.Text('Would you like to unblind your batch results file or your metadata sheet?',size=(100,1), font='Lucida', justification='left')],
        [sg.Frame(layout=[
            [sg.Radio('Batch Results File', 'RADIO2', default=False, key='_BatchFile_', enable_events=True, font=(14)), sg.Radio('Metadata Sheet', 'RADIO2', key='_Metadata_Sheet_', enable_events=True, font=(14))]], title='Options',title_color='black', relief=sg.RELIEF_SUNKEN)],
    [sg.Text('Select the file you would like to unblind: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left', visible='False'), sg.InputText('Select file', key = 'metadata_file', visible='False'), sg.FileBrowse()],
    [sg.Text('Select your blinding key: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left', visible='False'), sg.InputText('Select file', key = 'key_file', visible='False'), sg.FileBrowse()],
    [sg.Text('Select a folder to store your results: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left'),sg.InputText('Default Folder', key = '-results_folder-'), sg.FolderBrowse()],
     [sg.Text('Name your unblinded metadata sheet:', size=(50, 1), auto_size_text=False, justification='left', font=(12)),
    sg.InputText('Unblinded Metadata', key='-metadata_name-')],
    [sg.Text('_'  * 140)],
    [sg.Text('Would you like to unblind only the compound names, only the strain names, or both?',size=(100,1), font='Lucida', justification='left')],
        [sg.Frame(layout=[
            [sg.Radio('Compound', 'RADIO3', default=False, key='_Com_', enable_events=True, font=(14)), sg.Radio('Strain', 'RADIO3', key='_Strain_', enable_events=True, font=(14)), sg.Radio('Both', 'RADIO3', key='_Both_', enable_events=True, font=(14))]], title='Options',title_color='black', relief=sg.RELIEF_SUNKEN)],
        [sg.Button('Unblind'), sg.Button('Back')], [sg.Exit()]]
    
    u_win = sg.Window('Unblinding Metadata', layout4, size=(900,350), resizable=True, finalize=True)
    return u_win
    
def timelapse_window():
    layout4 = [
    [sg.Text('If you have time lapse analysis, you may add a time point collumn to your batch results file by using the time lapse key template that matches the file name to the time point',size=(120,1), font='Lucida', justification='left')],
    [sg.Text('Select your batch results file that you would like the time points collumn to be added to: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left', visible='False'), sg.InputText('Select file', key = 'filefortimelapse_', visible='False'), sg.FileBrowse()],
    [sg.Text('Select your time lapse key: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left', visible='False'), sg.InputText('Select file', key = 'timelapsekey_', visible='False'), sg.FileBrowse()],
    [sg.Text('Select a folder to store the new file: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left'),sg.InputText('Default Folder', key = '-tl_folder-'), sg.FolderBrowse()],
     [sg.Text('Name your file with the time points collumn:', size=(50, 1), auto_size_text=False, justification='left', font=(12)),
    sg.InputText('File with Time Points', key='-filenamewithtimelapse-')],
    [sg.Text('_'  * 140)],
        [sg.Button('Add TimePoints'), sg.Button('Back')], [sg.Exit()]]
    
    tl_win = sg.Window('Time Lapse Analysis Collumn', layout4, size=(900,250), resizable=True, finalize=True)
    return tl_win
    

def dataviz_options_window():
    layout5 = [
    [sg.Text('What is your independent variable?',size=(100,1), font='Lucida', justification='left')],
        [sg.Frame(layout=[
            [sg.Radio('Compound', 'RADIO2', default=False, key='_CompoundInfo_', enable_events=True, font=(14)), sg.Radio('Strain', 'RADIO2', key='_StrainInfo_', enable_events=True, font=(14)), sg.Radio('Time Lapse', 'RADIO2', key='_TimeLapse_', enable_events=True, font=(14))]], title='Options',title_color='black', relief=sg.RELIEF_SUNKEN)],
    [sg.Text('Select your batch results file: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left', visible='False'), sg.InputText('Select file', key = 'batch_results_file', visible='False'), sg.FileBrowse()],
    [sg.Text('Select the folder that contains your location files: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left'),sg.InputText('Default Folder', key = '-location_files_folder-'), sg.FolderBrowse()],
    [sg.Text('What is the name of your control variable:', size=(50, 1), auto_size_text=False, justification='left', font=(12)),
    sg.InputText('Control', key='-control_name-')],
    [sg.Text('_'  * 120)],
    [sg.Text('If you would like to restrict the variable you are not plotting, please make selections, otherwise click "None".')],
    [sg.Text('What type of variable would you like to restrict the independent variable under?',size=(100,1), font='Lucida', justification='left')],
        [sg.Frame(layout=[
            [sg.Radio('None', 'RADIO3', default=False, key='_none_select_', enable_events=True, font=(14)), sg.Radio('Compound', 'RADIO3', key='_compound_select_', enable_events=True, font=(14)), sg.Radio('Strain', 'RADIO3', key='_strain_select_', enable_events=True, font=(14)), sg.Radio('Both', 'RADIO3', default=False, key='_both_select_', enable_events=True, font=(14))]], title='Options',title_color='black', relief=sg.RELIEF_SUNKEN)],
    [sg.Text('Select the compound you want to restrict under:', size=(50, 1), auto_size_text=False, justification='left', font=(12)),
    sg.InputText('restricting compound', key='-compound-select-name-')],
    [sg.Text('Select the strain you want to restrict under:', size=(50, 1), auto_size_text=False, justification='left', font=(12)),
    sg.InputText('restricting strain', key='-strain-select-name-')],
    [sg.Text('_'  * 120)],
    [sg.Text('Would you like to select your colors?'), sg.Radio('Yes',  'RADIO4', default=False, key='yes_for_col_key', enable_events=True), sg.Radio('No', 'RADIO4', default=False, key='no_for_col_key', enable_events=True), sg.Text('If yes, please attach a colors key:', justification='left'), sg.InputText('Select file', key = 'col_key', justification='left', visible='False'), sg.FileBrowse()],
    [sg.Text('_'  * 120)],
    [sg.Text('Would you like to save your plot as a pdf file?', font=(9)), sg.Radio('Yes',  'RADIO5', default=False, key='yes_for_saving_pdf', enable_events=True), sg.Radio('No', 'RADIO5', default=False, key='no_for_saving_pdf', enable_events=True)], [sg.Text('If yes, select the folder in which you want to save your plot as a pdf file:', justification='left', visible='False', size=(50, 1), font=(9)),  sg.InputText('Select file', key = 'pdf_key', visible='False'), sg.FolderBrowse()],
    [sg.Text('If yes, please input a name for the pdf file:', auto_size_text=False, justification='left', size=(50, 1), font=(9)),
    sg.InputText('Data visualisation', key='-pdf_name_plot-')],
    [sg.Text(' '  * 120)],
    [sg.Button('Do Data Vis'), sg.Button('Back')], [sg.Exit()]]
    dataviz_options_win = sg.Window('Data Visualization Options', layout5, size=(900,600), resizable=True, finalize=True)
    return dataviz_options_win
    
    
def dataviz_twogroup_window():
    layout6 = [
    [sg.Text('What is your independent variable?',size=(100,1), font='Lucida', justification='left')],
        [sg.Frame(layout=[
            [sg.Radio('Compound', 'RADIO2', default=False, key='_CompoundInfo_', enable_events=True, font=(14)), sg.Radio('Strain', 'RADIO2', key='_StrainInfo_', enable_events=True, font=(14))]], title='Options',title_color='black', relief=sg.RELIEF_SUNKEN)],
    [sg.Text('Select your batch results file: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left', visible='False'), sg.InputText('Select file', key = 'batch_results_file', visible='False'), sg.FileBrowse()],
    [sg.Text('Select the folder that contains your location files: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left'),sg.InputText('Default Folder', key = '-location_files_folder-'), sg.FolderBrowse()],
    [sg.Text('What is the name of your control variable:', size=(50, 1), auto_size_text=False, justification='left', font=(12)),
    sg.InputText('Control', key='-control_name-')],
    [sg.Text('What is the name of your test variable:', size=(50, 1), auto_size_text=False, justification='left', font=(12)),
    sg.InputText('Test', key='-test_name-')],
    [sg.Button('Do Data Vis'), sg.Button('Back')], [sg.Exit()]]
    dataviz_twogroup_win = sg.Window('Data Visualization Options', layout6, size=(900,250), resizable=True, finalize=True)
    return dataviz_twogroup_win


#def dataviz_multitwo_window():
#    layout7 = [
#    [sg.Text('Are you doing a pairwise comparison between compounds or strains?',size=(100,1), font='Lucida', justification='left')],
#        [sg.Frame(layout=[
#            [sg.Radio('2 kinds of compounds', 'RADIO2', default=False, key='_CompoundInfo_', enable_events=True, font=(14)), sg.Radio('2 kinds of strains', 'RADIO2', key='_StrainInfo_', enable_events=True, font=(14))]], title='Options',title_color='black', relief=sg.RELIEF_SUNKEN)],
#    [sg.Text('Select your batch results file: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left', visible='False'), sg.InputText('Select file', key = 'batch_results_file', visible='False'), sg.FileBrowse()],
#    [sg.Text('Select the folder that contains your location files: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left'),sg.InputText('Default Folder', key = '-location_files_folder-'), sg.FolderBrowse()],
#    [sg.Text('What is the name of your control variable:', size=(50, 1), auto_size_text=False, justification='left', font=(12)),
#    sg.InputText('Control', key='-control_name-')],
#    [sg.Button('Do Data Vis'), sg.Button('Back')], [sg.Exit()]]
#    dataviz_multitwo_win = sg.Window('Data Visualization Options', layout7, size=(900,250), resizable=True, finalize=True)
#    return dataviz_multitwo_win
    
#def dataviz_multitwo_window():
#    layout7 = [
#    [sg.Text('What is your independent variable?',size=(100,1), font='Lucida', justification='left')],
#        [sg.Frame(layout=[
#            [sg.Radio('Compound', 'RADIO2', default=False, key='_CompoundInfo_', enable_events=True, font=(14)), sg.Radio('Strain', 'RADIO2', key='_StrainInfo_', enable_events=True, font=(14))]], title='Options',title_color='black', relief=sg.RELIEF_SUNKEN)],
#    [sg.Text('Select your batch results file: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left', visible='False'), sg.InputText('Select file', key = 'batch_results_file', visible='False'), sg.FileBrowse()],
#    [sg.Text('Select the folder that contains your location files: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left'),sg.InputText('Default Folder', key = '-location_files_folder-'), sg.FolderBrowse()],
#    [sg.Text('Please input the control - test pairs below. If you have less pairs than the number of questions, please leave the extra questions as it is.', size=(100, 1), auto_size_text=False, justification='left', font=(12))],
#    [sg.InputText('Control1', key='-control1_name-'), sg.InputText('Test1', key='-test1_name-')],
#    [sg.InputText('Control2', key='-control2_name-'), sg.InputText('Test2', key='-test2_name-')],
#    [sg.InputText('Control3', key='-control3_name-'), sg.InputText('Test3', key='-test3_name-')],
#    [sg.InputText('Control4', key='-control4_name-'), sg.InputText('Test4', key='-test4_name-')],
#    [sg.Button('Do Data Vis'), sg.Button('Back')], [sg.Exit()]]
#    dataviz_multitwo_win = sg.Window('Data Visualization Options', layout7, size=(900,250), resizable=True, finalize=True)
#    return dataviz_multitwo_win
    
def dataviz_multitwo_window():
    layout7 = [
    [sg.Text('What is your reference condition?',size=(100,1), font='Lucida', justification='left')],
        [sg.Frame(layout=[
            [sg.Radio('compound (I used 2 kinds of compounds)', 'RADIO2', default=False, key='_CompoundReference_', enable_events=True, font=(14)), sg.Radio('strains (I used 2 kinds of strains)', 'RADIO2', key='_StrainReference_', enable_events=True, font=(14))]], title='Options',title_color='black', relief=sg.RELIEF_SUNKEN)],
    [sg.Text('What are the 2 reference condition types?', size=(30, 1), auto_size_text=False, justification='left', font=(12)),
    sg.InputText('Reference 1', key='-ref1-'), sg.InputText('Reference 2', key='-ref2-')],
    [sg.Text('What factor do you want to compare?',size=(100,1), font='Lucida', justification='left')],
        [sg.Frame(layout=[
            [sg.Radio('compound ', 'RADIO3', default=False, key='_CompoundComparison_', enable_events=True, font=(14)), sg.Radio('strain ', 'RADIO3', key='_StrainComparison_', enable_events=True, font=(14))]], title='Options',title_color='black', relief=sg.RELIEF_SUNKEN)],
    [sg.Text('What is the name of your control variable in your comparison factor?', size=(50, 1), auto_size_text=False, justification='left', font=(12)),
    sg.InputText('Control', key='-control_name-')],
    [sg.Text('Select your batch results file: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left', visible='False'), sg.InputText('Select file', key = 'batch_results_file', visible='False'), sg.FileBrowse()],
    [sg.Text('Select the folder that contains your location files: ', size=(50, 1),font=(12) ,auto_size_text=False, justification='left'),sg.InputText('Default Folder', key = '-location_files_folder-'), sg.FolderBrowse()],
    [sg.Text('If you prefer to select your colors, attach a colors key, otherwise leave blank:', size=(50, 2),font=(12) ,auto_size_text=False, justification='left', visible='False'), sg.InputText('Select file', key = 'col_key', visible='False'), sg.FileBrowse()],
    [sg.Button('Do Data Vis'), sg.Button('Back')], [sg.Exit()]]
    dataviz_multitwo_win = sg.Window('Data Visualization Options', layout7, size=(900,400), resizable=True, finalize=True)
    return dataviz_multitwo_win
    
    
def check_fpaths(ipath, rpath):
        return True


### This funtion initiates the GUI
def make_GUI():
    win1 = make_win1()
    while True:
        event, values = win1.read()
        print(event)
        
        ### If exit button is clicked then the whole program is terminated
        if event in (None, 'Exit'):
            break
              
        

        ### Opens a window to analyze a batch of images
        ### Does not currently incorporate metadata for a batch of images but creates the fields to do so
        ### User is returned to the main page upon completion of analysis
        if event == '_IMG_ANALYSIS_':
            win1.hide()
            batch_win = make_batch_win()
            while True:
                e2, v2 = batch_win.read()
                if e2 in (None, 'Exit'):
                    batch_win.close()
                    break
                if e2 == '_README_':
                    webbrowser.open(RM_URL)
                if e2 == '_mdTemplate_':
                    webbrowser.open(MD_URL)
                if e2 == 'Analyze':
                    mdpath = (v2['md_file'])
                    rpath = (v2['-results_folder-'])
                    fpath = (v2['-image_folder-'])
                    results_name = (v2['-name-'])

                    im_path = plb.Path(fpath)
                    res_path = plb.Path(rpath)
                    
                    if im_path.exists() and res_path.exists():
                        ai.batch_process(fpath, rpath, mdpath, v2, e2, results_name)
                        batch_win.close()
                        make_GUI()
                        break
                    else:
                        sg.popup('Please enter a valid file or folder path')
                if e2 == 'Back':
                    batch_win.close()
                    make_GUI()
                    break
            batch_win.close()
            break
        
        ### Opens up a new window to analyze one image at a time.
        ### User can currently only add one strain and one compound to a plate
        ### User is not required to fill in a values for each plate
        # if values['_SINGLE_']:
        #     win1.hide()
        #     single_win = make_single_win()
        #     while True:
        #         e3, v3 = single_win.read()
        #         if e3 == 'Analyze':
        #             fpath = (v3['-file-'])
        #             rpath = (v3['-results-'])
        #             im_path = plb.Path(fpath)
        #             res_path = plb.Path(rpath)
        #             if im_path.exists() and res_path.exists():
        #                 ai.single_process(fpath, rpath, v3, e3)
        #                 single_win.close()
        #                 make_GUI()
        #                 break
        #             else:
        #                 sg.popup('Please enter a valid file or folder path')
        #         if e3 == 'Back':
        #             single_win.close()
        #             make_GUI()
        #             break
        #         if e3 in (None, 'Exit'):
        #             break
        #     single_win.close()
        #     break
            

        if values['_Yes_']:
            win1.hide()
            unblind = unblind_window()
            while True:
                e4, v4 = unblind.read()
                if e4 == 'Back':
                    unblind.close()
                    make_GUI()
                    break
                if e4 in (None, 'Exit'):
                    break
                if e4 == 'Unblind':
                    unblind_process(v4, unblind)
                    make_GUI()
                    break
            unblind.close()
            break
            
                
        if values['_DataVizSharedControl_']:
            win1.hide()
            dataviz_options = dataviz_options_window()
            while True:
                e5, v5 = dataviz_options.read()
                if e5 == 'Back':
                    dataviz_options.close()
                    make_GUI()
                    break
                if e5 == sg.WIN_CLOSED or e5 == 'Exit':
                    break
                if e5 == 'Do Data Vis':
                    batch_res = v5['batch_results_file']
                    loc_files_folder = v5['-location_files_folder-']
                    control_name = v5['-control_name-']
                    if v5['yes_for_saving_pdf']:
                        pdf_store_folder = v5['pdf_key']
                    else:
                        pdf_store_folder = 'Select file'
                    pdf_file_name = v5['-pdf_name_plot-']
                    if v5['yes_for_col_key']:
                        colors_key = v5['col_key']
                    else:
                        colors_key = 'None'
                    if v5['_none_select_']:
                        if colors_key != 'None':
                            colors = ck.dict_color_key(colors_key)
                        else:
                            colors = 'Select file'
                        if v5['_CompoundInfo_']:
                            dv.do_data_visualisation_compound(batch_res, loc_files_folder, control_name, colors, pdf_store_folder, pdf_file_name)
                        elif v5['_StrainInfo_']:
                            dv.do_data_visualisation_strain(batch_res, loc_files_folder, control_name, colors, pdf_store_folder, pdf_file_name)
                        elif v5['_TimeLapse_']:
                            dv.do_data_visualisation_timelapse(batch_res, loc_files_folder, control_name, colors, pdf_store_folder, pdf_file_name)
                    if colors_key != 'None':
                        colors = ck.dict_color_key_mutli2(colors_key)
                    else:
                        colors = 'Select file'
                    if v5['_StrainInfo_'] and v5['_compound_select_']:
                        selected_compound = v5['-compound-select-name-']
                        dv.data_viz_for_strain_under_1_compound(batch_res, loc_files_folder, control_name, selected_compound, colors, pdf_store_folder, pdf_file_name)
                    if v5['_CompoundInfo_'] and v5['_strain_select_']:
                        selected_strain = v5['-strain-select-name-']
                        dv.data_viz_for_compound_under_1_strain(batch_res, loc_files_folder, control_name, selected_strain, colors, pdf_store_folder, pdf_file_name)
                    if v5['_TimeLapse_'] and v5['_compound_select_']:
                        selected_compound = v5['-compound-select-name-']
                        dv.do_data_visualisation_timelapse_under_1compound(batch_res, loc_files_folder, control_name, selected_compound, colors, pdf_store_folder, pdf_file_name)
                    if v5['_TimeLapse_'] and v5['_strain_select_']:
                        selected_strain = v5['-strain-select-name-']
                        dv.do_data_visualisation_timelapse_under_1strain(batch_res, loc_files_folder, control_name, selected_strain, colors, pdf_store_folder, pdf_file_name)
                    if v5['_TimeLapse_'] and v5['_both_select_']:
                        selected_compound = v5['-compound-select-name-']
                        selected_strain = v5['-strain-select-name-']
                        dv.do_data_visualisation_timelapse_under_1compound_and_1strain(batch_res, loc_files_folder, control_name, selected_compound, selected_strain, colors, pdf_store_folder, pdf_file_name)
            dataviz_options.close()
            break
                    
                        
                        
        
        if values['_DataVizTwoGroup_']:
            win1.hide()
            dataviz_twogroup = dataviz_twogroup_window()
            while True:
                e6, v6 = dataviz_twogroup.read()
                if e6 == 'Back':
                    dataviz_twogroup.close()
                    make_GUI()
                    break
                if e6 == sg.WIN_CLOSED or e6 == 'Exit':
                    break
                if e6 == 'Do Data Vis':
                    batch_res = v6['batch_results_file']
                    loc_files_folder = v6['-location_files_folder-']
                    control_name = v6['-control_name-']
                    test_name = v6['-test_name-']
                    if v6['_CompoundInfo_']:
                        dv.do_data_visualisation_compound_2_group(batch_res, loc_files_folder, control_name, test_name)
                    elif v6['_StrainInfo_']:
                        dv.do_data_visualisation_strain_2_group(batch_res, loc_files_folder, control_name, test_name)
            dataviz_twogroup.close()
            break
                    
                        
        if values['_DataVizMultiTwo_']:
            win1.hide()
            dataviz_multitwo = dataviz_multitwo_window()
            while True:
                e7, v7 = dataviz_multitwo.read()
                if e7 == 'Back':
                    dataviz_multitwo.close()
                    make_GUI()
                    break
                if e7 == sg.WIN_CLOSED or e7 == 'Exit':
                    break
                if v7['_CompoundReference_'] or v7['_StrainComparison_']:
                    v7['_StrainComparison_'] = True
                    v7['_CompoundReference_'] = True
                    
                if v7['_StrainReference_'] or v7['_CompoundComparison_']:
                    v7['_CompoundComparison_'] = True
                    v7['_StrainReference_'] = True
                
                if e7 == 'Do Data Vis':
                    batch_res = v7['batch_results_file']
                    loc_files_folder = v7['-location_files_folder-']
                    reference_1 = v7['-ref1-']
                    reference_2 = v7['-ref2-']
                    colors_key = v7['col_key']
                    control_variable = v7['-control_name-']
                    if colors_key != 'Select file':
                        colors_key = ck.dict_color_key_mutli2(colors_key)
                    if v7['_CompoundReference_'] and v7['_StrainComparison_']:
                        dv.multi2group_dataviz_1(batch_res, loc_files_folder, control_variable, reference_1, reference_2, colors_key)
                    elif v7['_StrainReference_'] and v7['_CompoundComparison_']:
                        dv.multi2group_dataviz_2(batch_res, loc_files_folder, control_variable, reference_1, reference_2, colors_key)
            dataviz_multitwo.close()
            break
        
        if values['_TimeLapseCollumn_']:
            win1.hide()
            tl_window = timelapse_window()
            while True:
                e8, v8 = tl_window.read()
                if e8 == 'Back':
                    tl_window.hide()
                    make_GUI()
                if e8 in ('Exit', None):
                    break
                if e8 == 'Add TimePoints':
                    file = v8['filefortimelapse_']
                    key = v8['timelapsekey_']
                    name = v8['-filenamewithtimelapse-']
                    folder = v8['-tl_folder-']
                    tl.timelapse_collumn_addition(file, key, folder, name)
                    message_win()
                    tl_window.close()

                    
                    
                    
    win1.close()
    
    
    
def unblind_process(v4, unblind):
    metapath = (v4['metadata_file'])
    keypath = (v4['key_file'])
    rpath = (v4['-results_folder-'])
    name = v4['-metadata_name-']
    m_path = plb.Path(metapath)
    r_path = plb.Path(keypath)
    f_path = plb.Path(rpath)
    if m_path.exists() and r_path.exists():
        if v4['_Metadata_Sheet_']:
            if v4['_Com_']:
                un.solve_compound_names(metapath, keypath, rpath, name)
            elif v4['_Strain_']:
                un.solve_strain_names(metapath, keypath, rpath, name)
            elif v4['_Both_']:
                un.solve_both_strain_and_compound_names(metapath, keypath, rpath, name)
        if v4['_BatchFile_']:
            if v4['_Com_']:
                un.solve_compound_names_batchres(metapath, keypath, rpath, name)
            elif v4['_Strain_']:
                un.solve_strain_names_batchres(metapath, keypath, rpath, name)
            elif v4['_Both_']:
                un.solve_both_strain_and_compound_names_batchres(metapath, keypath, rpath, name)
    else:
        sg.popup('Please enter valid files')
    message_win()
    unblind.close()



def message_win():
    layout = [[sg.Text('Done!', size=(60, 1), justification='center', font=(14))], [sg.OK()]]
    window = sg.Window('Message', layout, size=(400, 60))
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'OK'):
            window.close()
            break
        break

def main():
    make_GUI()

if __name__ == '__main__':
    main()
