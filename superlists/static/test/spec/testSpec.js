    describe('fixture-test', function () {
        beforeEach(function() {
            loadFixtures('keske.html');
        });

        it('error should not be hidden before click', function () {
            expect($('.has-error')).toBeVisible();
        });

        it('hide on press', function () {
            $('input').trigger('keypress');
            //$('.has-error').hide();
            expect($('.has-error')).not.toBeVisible();
        });
    });
