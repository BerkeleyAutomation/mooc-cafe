// accounts.js
// Handles authentication, registration, login
// Dependencies: jQuery

var accounts = (function($, d3, console) {
    // Enable strict javascript interpretation
    "use strict";
    // a function to pull up the registration prompt

    function showRegister() {
        $('.register').show();
        $('#finishRegistration').click(function() {});
    }

    function showCommentInput() {
        $('.comment-input').show();
    }

    // a function to pull up the login prompt.

    function showLogin() {
        $('.landing').hide();
        $('.login').show();
    }

    //function that determines if the user has already rated 2 comments
    // and should now login/ register to move forward.

    function readyToLogin() {
        return window.ratings && window.ratings.length >= 2;
    }

    // function that determines if the user should register to continue
    // it returns true when both the registration sliders have been saved.

    function mustRegister() {
        return window.sliders && window.sliders.length >= 1;
    }

    //function that removes the landing page and populates the map when the first time button is clicked.

    function firstTime() {
        utils.showLoading("Loading the garden...", function() {
            blooms.populateBlooms();

            setTimeout(function() { // d3 needs a little extra time to load
                $('.landing').hide();
            }, 1500);
        });
    }
    // Checks to see if the user has logged in and sets window.authentiated.
    // This is used to change the behavior of the site for users
    // that have logged in. (Mostly to send data to server immediately)

    function setAuthenticated() {
        $.ajax({
            async:false,
            type: "GET",
            dataType: 'json',
            url: window.url_root + '/os/testAuth/',
            success: function(data) {
                window.authenticated = data['is_user_authenticated'];
            },
            error: function() {
                console.log("didn't get sent!");
            }
        });

        return window.authenticated;
    }

    //@logindata - data is in a serialized form
    //This function is used specifically to login right after registration. This function also
    //  sends the data that has been stored in the window to the server after a successful the login.

    function loginAfterRegister(loginData) {
        $.ajax({
            async : false,
            url: window.url_root + '/accountsjson/login/',
            type: 'POST',
            dataType: 'json',
            data: loginData,
            success: function(data) {
                if (data.hasOwnProperty('success')) {
                    console.log("successful login detected!!");
                    window.authenticated = true;
                    //rate.sendComment(window.comment);
                    rate.logUserEvent(0,'login');
                    for (var i = 1; i <= window.num_sliders; i++) {
                        rate.sendSlider(window.sliders[i], i);
                        //blooms will be populated at the end of this! see callback
                        //there are two calls!!
                    }
                    accounts.initLoggedInFeatures(true);
                    
                    //for (i = 0; i < window.ratings.length - 1; i++) {
                    //    rate.sendAgreementRating(window.ratings[i]);
                    //    rate.sendInsightRating(window.ratings[i]);
                    //}

                    //rate.sendAgreementRating(window.ratings[window.ratings.length - 1]);
                    //rate.sendInsightRating(window.ratings[window.ratings.length - 1]);
                    //window.authenticated = true;
                } else {
                    // we should rerender the form here.
                }
            },
            error: function() {
                console.log("ERROR posting login request. Abort!");
            }
        });
    }


    function loadMyCommentDiv() {
        $.ajax({
            async:false,
            type: "GET",
            dataType: 'json',
            url: window.url_root + '/os/show/1/',
            success: function(data) {
                try {
                    var comment = data['cur_user_comment'][0][0];
                    $('#entered-comment').html(comment);
                } catch (err) {
                    // probably an admin user or something. they didn't have a comment
                }
                $('.my-comment').show();
        $('.menubar').find('.ui-btn-active').removeClass('ui-btn-active ui-focus');
                
            },
            error: function() {
                console.log("didn't get sent!");
            }
        });


    }

    /** Sets the field ".num-rated-by" to the number of people who've rated the 
     *  users comment. */

    function setNumRatedBy() {
        $.ajax({
            async:false,
            type: "GET",
            dataType: 'json',
            url: window.url_root + '/os/ratedby/1/',
            success: function(data) {
                $('.num-rated-by').text(data['sorted_comments_ids'].length);
            },
            error: function() {
                console.log("didn't get sent!");
            }
        });
    }

    function skipStatement(id) {

    if(window.skipped[id-1])
    {
    $('#s'+id).removeAttr('disabled');
        document.getElementById('tr-slider'+id).style.backgroundColor='transparent';
        document.getElementById('tr-label'+id).style.backgroundColor='#f5ebdf';
        document.getElementById('tr-1grade'+id).style.backgroundColor='#f5ebdf';
        document.getElementById('tr-2grade'+id).style.backgroundColor='#f5ebdf';
        document.getElementById('skip-img'+id).src = window.url_root + '/media/mobile/img/cafe/skip.png';
        document.getElementById('skip-img'+id).style.width = '50px';
        window.skipped[id-1] = false;
        rate.logUserEvent(11,'slider_set ' + id + ' ' + 'grade');
    }
    else
    {
    $('#s'+id).attr('disabled', 'disabled');
    document.getElementById('tr-slider'+id).style.backgroundColor='#BFBFBF';
    document.getElementById('tr-label'+id).style.backgroundColor='#BFBFBF';
    document.getElementById('tr-1grade'+id).style.backgroundColor='#BFBFBF';
    document.getElementById('tr-2grade'+id).style.backgroundColor='#BFBFBF';
    document.getElementById('skip-img'+id).src = window.url_root + '/media/mobile/img/cafe/grade.png';
    document.getElementById('skip-img'+id).style.width = '50px';
    window.skipped[id-1] = true;
    rate.logUserEvent(11,'slider_set ' + id + ' ' + 'skip');
    }

    }

    /** Sets up all the stuff that loggedIn users expect and need. 
     *  JUSTREGISTERED is a boolean and optional. Used to shortcircuit showGraphs.
     */

    function initLoggedInFeatures(justRegistered) {
        $('.top-bar').show();
        justRegistered = typeof justRegistered !== 'undefined' ? justRegistered : false;
        $('#regzip').prop('disabled', true);
        //utils.ajaxTempOff(function() {

            //seems slow TODO
            //stats.showGraphs(justRegistered);


        $.ajax({
            async:false,
            type: "GET",
            dataType: 'json',
            url: window.url_root + '/os/show/1/',
            success: function(data) {
                $('.score-value').text("" + ~~(data['cur_user_rater_score'] * window.conf.SCORE_SCALE_FACTOR));
                window.user_score = data['cur_user_rater_score'];
                $('.username').text(' ' + data['cur_username']);
                if (window.user_score == 0) {
                            accounts.hideAll();
                            $('.dialog').show();
                            window.cur_state = 'register';
                            window.prev_state = 'dialog';
                        } else {
                            accounts.hideAll();
                            $('.menubar').show();
                            window.cur_state = 'map';
                            window.prev_state = 'map';
                        }
            },
            error: function() {
                console.log("didn't get sent!");
            }
        });
    }
    
    function sendEmail(mail){
		
		$.ajax({
            type: "POST",
            dataType: 'json',
            url: window.url_root + "/confirmationmail/",
            data: {'mail':mail},
            success: function(data) {
                if (data.hasOwnProperty('success')) {
                    //console.log("data was sent!")
                    window.email_saved = true;
                    $('.dialog-email').show();
                    window.cur_state = 'email';
                    $('.dialog-continue').hide();
                    $("#email-error").hide();
                    window.prev_state = 'continue';
                }
                else{

                 $("#email-error").show();
                 $("#email-error").text(data['error']);
                 console.log(data['error']);

                }
            }
        });
	}
	
	function getNeighborStat(){
		
		/*$.ajax({
          type: "POST",
          dataType: 'json',
          url: window.url_root + "/neighborhoodStat/",
          data: {'zipcode':window.conf.ZIPCODE},
          success: function(data) {
	      
		  $('#neighborhoodTable').html(data.html);
          if (data.hasOwnProperty('success')) {
            //console.log("data was sent!")
            }
          },
          error: function() {
			  console.log("code error");
               }
          });*/
	}

	function hideAll(){
	    $('.register').hide();
	    $('.landing').hide();
        $('.endsliders').hide();
        $('.dialog').hide();
        $('.dialog-avggrade').hide();
        $('.dialog-about').hide();
        $('.comment-input').hide();
        $('.menubar').hide();
        $('.rate').hide();
        $('.dialog-continue').hide();
        $('.dialog-email').hide();
        $('.my-comment').hide();
        $('.dialog-help-alt').hide();
        $('.dialog-help-grade').hide();
        $('.dialog-help-median').hide();
        $('.dialog-help-zipcode').hide();
        $('.dialog-help-dialog').hide();
        $('.dialog-help-map1').hide();
        $('.dialog-help-map2').hide();
        $('.dialog-help-map3').hide();
        $('.dialog-help-rate').hide();
        $('.dialog-help-comment').hide();
        $('.dialog-help-continue').hide();
        $('.dialog-help-logout').hide();
	}

    return {
        'showCommentInput': showCommentInput,
        'showRegister': showRegister,
        'showLogin': showLogin,
        'readyToLogin': readyToLogin,
        'mustRegister': mustRegister,
        'skipStatement':skipStatement,
        'firstTime': firstTime,
        'setAuthenticated': setAuthenticated,
        'loginAfterRegister': loginAfterRegister,
        'loadMyCommentDiv': loadMyCommentDiv,
        'initLoggedInFeatures': initLoggedInFeatures,
        'sendEmail': sendEmail,
        'getNeighborStat': getNeighborStat,
        'hideAll': hideAll
    };

})($, d3, console);

$(document).ready(function() {
    $('#reg_form').submit(function(e) {
        $('#register').find('.ui-btn-active').removeClass('ui-btn-active ui-focus');
        e.preventDefault();
        e.stopPropagation();

        if(window.authenticated)
        {
            accounts.hideAll();
            $('.dialog').show();
            return;
        }

        rate.logUserEvent(9,'register');

        if (window.registration_in_progress) {
            return;
        }
        else{
            window.registration_in_progress = true;
        }

        $("#username-error").hide();
        $("#password-error").hide();
        $("#zipcode-error").hide();

        /*Let us leave this to the server to handle
        // Handle bad length zipcodes client-side
        if ($('#regzip').val().length != 5) {
            $("#zipcode-error").html("Please enter a 5 digit zipcode.");
            $("#zipcode-error").show();
            $('#registerpanel').find('.ui-btn-active').removeClass('ui-btn-active ui-focus');
            return;
        }*/
        
        var registrationData = {
            "username": $('#regusername').val(),
            "password": $('#regpassword1').val(),
            "password1": $('#regpassword1').val(),
            "password2": $('#regpassword1').val(),
            "email": $('#regemail').val(),
            "zipcode" : ($('#regzip').val() == '')?'-1':$('#regzip').val()
        };

        var loginData = {
            "username": registrationData.username.toLowerCase(),
            "password": registrationData.password,
        };

        //utils.ajaxTempOff(function() {
            $.ajax({
                async:false,
                url: window.url_root + '/accountsjson/register/',
                type: 'POST',
                dataType: 'json',
                data: registrationData,
                success: function(data) {
                    $("#username-error").hide();
                    //$("#email-error").hide();
                    $("#password-error").hide();

                    window.registration_in_progress = false;

                    if (data.hasOwnProperty('success')) {
                        accounts.setAuthenticated();
                        utils.showLoading("Loading", function() {
                            accounts.loginAfterRegister(loginData);
                            blooms.populateBlooms();
                            $('.register').hide();
                            $("#regzip").attr("disabled", true);
                            utils.hideLoading();
                            window.conf.ZIPCODE=registrationData.zipcode;
                            window.prev_state = 'register';
                            window.cur_state = 'dialog';

			                //Slow TODO
			                //accounts.getNeighborStat();

                            /*setTimeout(function() { //give d3 some extra time
                                $('.register').slideUp('fast', function() {
                                    utils.hideLoading(500);
                                });
                            }, 500);*/
                        });
                        //accounts.setAuthenticated();
                    } else {
                        accounts.showRegister();
                        if (data.hasOwnProperty('form_errors')) {

                            var errors = data['form_errors'];

                            if ('username' in errors) {
                                $("#username-error").html(errors['username']);
                                $("#username-error").show();
                            }

                            /* if ('email' in errors) {
                                $("#email-error").html(errors['email']);
                                $("#email-error").show();
                            }*/

                            if ('password1' in errors) {
                                $("#password-error").html(errors['password1']);
                                $("#password-error").show();
                            }

                            try {
                            //TODO: why doesn't this come up under form_errors[zip_code]
                                if (data['form_errors']['__all__'][0]) {
                                    $("#zipcode-error").html(data['form_errors']['__all__'][0]);
                                    $("#zipcode-error").show();
                                }
                            } catch(err) { }

                        }
                    }
                },
                error: function() {
                    console.log("ERROR posting registration request. Abort!");
                },
            });
        //});
    });

    $('#login_form').submit(function(e) {
        e.preventDefault();
        e.stopPropagation();

        var serializedFormData = $(this).serialize();

            $.ajax({
                async: false,
                url: window.url_root + '/accountsjson/login/',
                type: 'POST',
                dataType: 'json',
                data: serializedFormData,
                success: function(data) {
                    $("#login-error").hide();

                    if (data.hasOwnProperty('success')) {
                        accounts.setAuthenticated();
                        utils.showLoading("Loading...", function() {
                            blooms.populateBlooms();
                            accounts.initLoggedInFeatures();
                            $('.top-bar').show();

                            setTimeout(function() { // d3 needs a little extra time to load
                                $('.login').hide();
                            }, 1000);
                        });
                    } else {
                        console.log("Failed login attempt");
                        $('#login-error').text(data['form_errors'].__all__[0]);
                        $("#login-error").show();
                        $('#login').find('.ui-btn-active').removeClass('ui-btn-active ui-focus');

                    }
                },
                error: function() {
                    console.log("ERROR posting login request. Abort!");
                }
            });
        

    });

    $('.first-time-btn').click(function() {
        //accounts.firstTime();
        window.history.pushState("", "", '#');
        accounts.hideAll();
        $('.endsliders').show();
        window.cur_state = 'grade';
        rate.logUserEvent(7,'first time');
        //$('.top-bar').show();
        //rate.initScore();
    });

    $('.login-btn').click(function() {
        accounts.showLogin();
    });

    $('.home-btn-dialog').click(function() {
           window.no_menubar = true;
           $('.landing-navigation').show();
           accounts.hideAll();
           window.prev_state = window.cur_state;
           window.cur_state = 'home';
           if (window.authenticated){
              $('.landing').show();
              $('.menubar').hide();
              $('.scorebox').hide();
           }
           else{
              $('.landing').show();
              $('.menubar').hide();
           }
        });


    var backButtonHandler = function() {
               window.cur_state = window.prev_state;
               if (window.prev_state == 'home'){
                  $('.landing').show();
                  window.prev_state = 'home';
               }
               else if (window.prev_state == 'grade')
               {
                  $('.endsliders').show();
                  window.prev_state = 'home';
                }
                else if (window.prev_state == 'median')
                 {
                    $('.dialog-avggrade').show();
                    window.prev_state = 'grade';
                }
                else if (window.prev_state == 'rate')
                {
                  $('.rate').show();
                  window.prev_state = 'map';
                }
                else if (window.prev_state == 'register')
                {
                  $('.register').show();
                  window.prev_state = 'grade';
                }
                else if (window.prev_state == 'dialog')
                {
                  $('.dialog').show();
                  window.prev_state = 'register';
                }
                else if (window.prev_state == 'map')
                {
                    window.prev_state = 'dialog';
                    $('.menubar').show();
                    //$('.scorebox').show();
                }
                else if (window.prev_state == 'comment')
                {
                    window.prev_state = 'map';
                    $('.comment-input').show();
                }
                else if (window.prev_state == 'continue')
                {
                   window.prev_state = 'comment';
                   $('.dialog-continue').show();
                }
                else if (window.prev_state == 'email')
                {
                   window.prev_state = 'continue';
                   $('.dialog-email').show();
                }
                else if (window.prev_state.indexOf('help') != -1)
                {
                    $('.dialog-help-alt').show();
                    window.prev_state = window.prev_state.substring(4);
                }
                else if (window.prev_state == 'stats')
                {

                    //window.location = window.url_root.substring(0,window.url_root.length)+'/crcstats/' + window.refer;
                    //$('.scorebox').show();
                }

               window.scrollTo(0,0);
                window.history.pushState("", "", '#');


            }

    $('.back-btn-dialog').click(function(){accounts.hideAll();backButtonHandler();});

    $('.help-btn-dialog').click(function() {
                                 if (window.cur_state.indexOf('help') != -1)
                                 {
                                    return;
                                 }
                                 accounts.hideAll();
                                 window.prev_state = window.cur_state;
                                 window.cur_state = 'help-' + window.cur_state;
                                 if (window.cur_state == 'help-home')
                                 {
                                    $('.dialog-about').show();
                                 }
                                 else if (window.cur_state == 'help-grade')
                                 {
                                    $('.dialog-help-grade').show();
                                 }
                                 else if (window.cur_state == 'help-median')
                                  {
                                     $('.dialog-help-median').show();
                                  }
                                 else if (window.cur_state == 'help-register')
                                  {
                                     $('.dialog-help-zipcode').show();
                                  }
                                 else if (window.cur_state == 'help-dialog')
                                  {
                                      $('.dialog-help-dialog').show();
                                  }
                                 else if (window.cur_state == 'help-map')
                                 {
                                      if(window.user_score < 2)
                                        $('.dialog-help-map1').show();
                                      else if ($('.instructions3').css('display') != 'none')
                                        $('.dialog-help-map2').show();
                                      else
                                        $('.dialog-help-map3').show();

                                      console.log(window.user_score)
                                 }
                                 else if (window.cur_state == 'help-rate')
                                 {
                                       $('.dialog-help-rate').show();
                                 }
                                 else if (window.cur_state == 'help-comment')
                                 {
                                      $('.dialog-help-comment').show();
                                 }
                                 else if (window.cur_state == 'help-continue')
                                 {
                                      $('.dialog-help-continue').show();
                                 }
                                 else if (window.cur_state == 'help-logout')
                                 {
                                     $('.dialog-help-logout').show();
                                 }
                                 else{
                                    $('.dialog-help-alt').show();
                                 }

                             });

    $('.login-form-go-back').click(function() {
        $('.landing').show();
        $('.login').hide();
    });

    $('.my-comment-btn').click(function() {
        accounts.loadMyCommentDiv();
        $('.scorebox').hide();
        $('.menubar').hide();
        window.prev_state = 'map';
    });

    $('.edit-comment-btn').click(function() {
        $('.comment-region').hide();
        $('.edit-comment').show();
    });
    
    $('#flag1').click(function() {

        if(window.toggle_flag1)
        {
            window.toggle_flag1 = false;
            document.getElementById('flag').innerHTML='';
            document.getElementById('flag1').innerHTML='Inappropriate';
            return;
        }

        window.toggle_flag1 = true;
        document.getElementById('flag').innerHTML='Flagged for Review';
        document.getElementById('flag1').innerHTML='Undo';
            $.ajax({
            type: "POST",
            url: window.url_root + "/os/flagcomment/1/"+window.current_cid+"/",
            success: function(data) {
                if (data.hasOwnProperty('success')) {
                    console.log("flag successfully sent");
                }
            },
            error: function() {
                console.log("ERROR flag didn't get sent");
            }
        });
    });

    $('#flag2').click(function() {
            if(window.toggle_flag2)
                    {
                        window.toggle_flag2 = false;
                        document.getElementById('flag').innerHTML='';
                        document.getElementById('flag2').innerHTML='Irrelevant';
                        return;
                    }
            window.toggle_flag2 = true;
            document.getElementById('flag').innerHTML='Flagged for Review';
            document.getElementById('flag2').innerHTML='Undo';
                $.ajax({
                type: "POST",
                url: window.url_root + "/os/flagcomment/1/"+window.current_cid+"/",
                success: function(data) {
                    if (data.hasOwnProperty('success')) {
                        console.log("flag successfully sent");
                    }
                },
                error: function() {
                    console.log("ERROR flag didn't get sent");
                }
            });
        });

    $('.dialog-ready').click(function() {
        rate.logUserEvent(8,'dialog 1');
        rate.initMenubar();
        //$('.scorebox').show();

        if(window.user_score == 0)
        {
            $('.instructions').show();
        }

        $('.dialog').hide();
        window.prev_state = 'dialog';
        window.cur_state = 'map';
    });
    
    $('.dialog-score-ready').click(function() {
        rate.logUserEvent(8,'dialog 2');
        $('.dialog-score').hide();
        //$('.scorebox').show();
        rate.initMenubar();
        //rate.initMenubar();
    });

    $('.dialog-continue-ready').click(function() {
            rate.logUserEvent(8,'dialog 3');
            
            //$('.scorebox').show();
            if ($('#regemail').val()){
                    accounts.sendEmail($('#regemail').val());
           	}
           	else
           	{
           	    rate.initMenubar();
           	    window.prev_state = 'continue';
           	    window.cur_state = 'map';
           	    $('.dialog-continue').hide();
           	    window.your_mug.transition().duration(2000).style("opacity", "0.4");
           	}
        });

        $('.dialog-email-ready').click(function() {
                rate.logUserEvent(8,'dialog 4');
                $('.dialog-email').hide();
                rate.initMenubar();
                window.prev_state = 'email';
                window.cur_state = 'map';
                window.your_mug.transition().duration(2000).style("opacity", "0.4");
            });
    
    $('.dialog-yourmug-ready').click(function() {
        rate.logUserEvent(8,'dialog 4');
        $('.dialog-yourmug').hide();
        //$('.scorebox').show();
        $('.menubar').show();
        /*try{
            window.your_mug.transition().duration(1000).style("opacity", "1");
        }catch(err){
            console.log(err);
        }*/
    });


    $('.edit-comment-save-btn').click(function() {
        rate.sendComment($('.edit-comment-box').val());
        $('.menubar').find('.ui-btn-active').removeClass('ui-btn-active ui-focus');

        $('.my-comment').hide();
    });

    $('.edit-comment-cancel-btn').click(function() {
        $('.comment-region').show();
        $('.edit-comment').hide();
    });

    $('.edit-comment-done-btn').click(function() {
        $('.menubar').find('.ui-btn-active').removeClass('ui-btn-active ui-focus');
        $('.my-comment').hide();
        //$('.scorebox').show();
    });

    $('.logout-btn').click(function(e) {
        rate.logUserEvent(1,'logout');
        accounts.hideAll();
        window.cur_state = 'logout';
        window.prev_state = 'logout';

        $('.logout').show();
        e.preventDefault();
        e.stopPropagation();
        window.history.pushState("", "", '/mobile');

        $.ajax({
            url: window.url_root + '/accountsjson/logout/',
            type: 'POST',
            dataType: 'json',
            success: function(data) {
                if (data.hasOwnProperty('success')) {
                    // TODO: this needs to be cleaned up into some sort of function
                    // and this logic is shitty and it's not resetting the score labels well
                    //$('.landing').show();
                    window.user_score = undefined;
                    window.authenticated = false;
                    $('.menubar').hide();
                    rate.resetEndSliders();
                } else {}
            },
            error: function() {
                console.log("ERROR posting login request. Abort!");
            }
        });

    });

    $('.logout-start-over').click(function() {
	    window.location = window.url_root + "/mobile/";
    });

    $('.logout-login-again').click(function() {
        $('.logout').hide();
        $('.login').show();
    });
    
    $('#regrade-btn').click(function(){
		$('.welcome-back').hide();
		$('.endsliders').show();
	});
	
	$('#garden-btn').click(function(){
		$('.welcome-back').hide();
		if(!window.no_menubar)
           {
               $('.menubar').show();
               $('.scorebox').show();
           }
        window.no_menubar = false;
	});

    window.onpopstate = function(event) {
        backButtonHandler();
    };
});
