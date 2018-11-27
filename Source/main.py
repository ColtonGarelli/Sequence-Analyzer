import Director


def UI_main(director):
    done = False
    input_source = director.start_up()
    first_time = True
    seq_list: list
    while not done:
        # while loop terminates when done = True
        if first_time:
            # if first time is true, the following options set up input
            if input_source == "1":
                seq_list = director.db_access()
                director.set_master_list(seq_list)
            elif input_source == "2":
                seq_list = director.handle_manual_input()
                director.set_master_list(seq_list)
            elif input_source == "0":
                break
        else:
            pass
        first_time = False
        choice = director.view_or_process()
        while choice == 'v':
            # interface to view
            # todo: options to change view
            choice = director.view_or_process()

        if input_source != '0':
            bias_data = director.run_bias_analysis()
            fells_data = director.run_FELLS_analysis()
            soda_data = director.run_SODA_analysis()
            if not isinstance(fells_data, dict):
                director.update_seq_data(fells=fells_data, soda=soda_data, sec_bias=bias_data)
            director.view_analysis()
            write_dict = director.seqrecord_to_dict(seq_list)
            file_path = director.write_dict_to_file(write_dict)
            done = director.quit_or_continue()
        else:
            break


if __name__ == '__main__':
    main_director = Director.Director()

    UI_main(main_director)
