for module in ["qcd","data"]:
	exec ("from __%s__ import %s"%(module,module))
