import supervisor

def exit_to_shell():
	supervisor.reload()

def load_next(location):
	supervisor.set_next_code_file(location)