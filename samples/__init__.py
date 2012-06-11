for module in ["qcd","data","sigmc"]:
	exec ("from __%s__ import %s"%(module,module))
