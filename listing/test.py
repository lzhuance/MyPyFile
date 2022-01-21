from gnss_cmn.crd_conv import xyz2llh,llh2xyz

# test
xyz = [4097216.5288899, 4429119.2189355, -2065771.1625112]
llh = [-19.01830416341792, 47.229213976631534, 1552.9602058911696]
print(xyz2llh(xyz))
print(llh2xyz(llh))
