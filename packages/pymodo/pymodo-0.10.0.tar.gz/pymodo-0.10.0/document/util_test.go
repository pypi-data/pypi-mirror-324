package document

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestAppendNew(t *testing.T) {
	sl1 := make([]int, 0, 32)
	sl1 = append(sl1, 1, 2)

	sl2 := appendNew(sl1, 3, 4)

	assert.Equal(t, []int{1, 2}, sl1)
	assert.Equal(t, []int{1, 2, 3, 4}, sl2)
}

func TestWarnOrError(t *testing.T) {
	assert.Nil(t, warnOrError(false, "%s", "test"))
	assert.NotNil(t, warnOrError(true, "%s", "test"))
}

func TestLoadTemplates(t *testing.T) {
	f := TestFormatter{}
	templ, err := LoadTemplates(&f, "../docs/docs/templates")
	assert.Nil(t, err)

	assert.NotNil(t, templ.Lookup("package.md"))
}
