local vt = require('test/vector')
local log = require('test/log')
local util = require('test/test_util')


local function test_Clone()
    local vt_a = util.CreateVector(1)
    local vt_b = vt.Clone(vt_a)
    assert(vt_a.mask == vt_b.mask, 'clone mask failed.')
end
local function test_Append()
    local vt_a = util.CreateVector(2)
    local si = util.CreateSignal()
    vt.Append(vt_a, si)
    assert(#vt_a.signals == 3, 'failed')
end

test_Append()
-- print(sl.Pretty(CreateSignal()))
-- test_Clone()