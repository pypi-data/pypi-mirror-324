drop table if exists `tcs_cat_ps1_medium_deep_ref`;

create table `tcs_cat_ps1_medium_deep_ref` (
`id` bigint(20) unsigned NOT NULL,
`mdfield` varchar(10) NOT NULL,
`ra` double NOT NULL,
`decl` double NOT NULL,
`ipp_idet_g` int(10) unsigned,
`psf_inst_mag_g` float,
`psf_inst_mag_sig_g` float,
`ap_mag_g` float,
`ap_mag_radius_g` float,
`peak_flux_as_mag_g` float,
`cal_psf_mag_g` float,
`cal_psf_mag_sig_g` float,
`sky_g` float,
`sky_sigma_g` float,
`psf_chisq_g` float,
`cr_nsigma_g` float,
`ext_nsigma_g` float,
`psf_major_g` float,
`psf_minor_g` float,
`psf_theta_g` float,
`psf_qf_g` float,
`psf_ndof_g` int(11),
`psf_npix_g` int(11),
`moments_xx_g` float,
`moments_xy_g` float,
`moments_yy_g` float,
`flags_g` int(10) unsigned,
`n_frames_g` smallint(5) unsigned,
`padding_g` smallint(6),
`psf_inst_flux_g` float,
`psf_inst_flux_sig_g` float,
`ap_flux_g` float,
`ap_flux_sig_g` float,
`ap_mag_raw_g` float,
`flags2_g` int(10) unsigned,
`kron_flux_g` float,
`kron_flux_err_g` float,
`kron_flux_inner_g` float,
`kron_flux_outer_g` float,
`moments_r1_g` float,
`moments_rh_g` float,
`psf_qf_perfect_g` float,
`fpa_filter_g` varchar(80),
`mjd_obs_g` double,
`exptime_g` double,
`imageid_g` int(11),
`zero_pt_g` double,
`delta_mag_g` float,
`no_of_filter_values_g` int,
`ipp_idet_r` int(10) unsigned,
`psf_inst_mag_r` float,
`psf_inst_mag_sig_r` float,
`ap_mag_r` float,
`ap_mag_radius_r` float,
`peak_flux_as_mag_r` float,
`cal_psf_mag_r` float,
`cal_psf_mag_sig_r` float,
`sky_r` float,
`sky_sigma_r` float,
`psf_chisq_r` float,
`cr_nsigma_r` float,
`ext_nsigma_r` float,
`psf_major_r` float,
`psf_minor_r` float,
`psf_theta_r` float,
`psf_qf_r` float,
`psf_ndof_r` int(11),
`psf_npix_r` int(11),
`moments_xx_r` float,
`moments_xy_r` float,
`moments_yy_r` float,
`flags_r` int(10) unsigned,
`n_frames_r` smallint(5) unsigned,
`padding_r` smallint(6),
`psf_inst_flux_r` float,
`psf_inst_flux_sig_r` float,
`ap_flux_r` float,
`ap_flux_sig_r` float,
`ap_mag_raw_r` float,
`flags2_r` int(10) unsigned,
`kron_flux_r` float,
`kron_flux_err_r` float,
`kron_flux_inner_r` float,
`kron_flux_outer_r` float,
`moments_r1_r` float,
`moments_rh_r` float,
`psf_qf_perfect_r` float,
`fpa_filter_r` varchar(80),
`mjd_obs_r` double,
`exptime_r` double,
`imageid_r` int(11),
`zero_pt_r` double,
`delta_mag_r` float,
`no_of_filter_values_r` int,
`ipp_idet_i` int(10) unsigned,
`psf_inst_mag_i` float,
`psf_inst_mag_sig_i` float,
`ap_mag_i` float,
`ap_mag_radius_i` float,
`peak_flux_as_mag_i` float,
`cal_psf_mag_i` float,
`cal_psf_mag_sig_i` float,
`sky_i` float,
`sky_sigma_i` float,
`psf_chisq_i` float,
`cr_nsigma_i` float,
`ext_nsigma_i` float,
`psf_major_i` float,
`psf_minor_i` float,
`psf_theta_i` float,
`psf_qf_i` float,
`psf_ndof_i` int(11),
`psf_npix_i` int(11),
`moments_xx_i` float,
`moments_xy_i` float,
`moments_yy_i` float,
`flags_i` int(10) unsigned,
`n_frames_i` smallint(5) unsigned,
`padding_i` smallint(6),
`psf_inst_flux_i` float,
`psf_inst_flux_sig_i` float,
`ap_flux_i` float,
`ap_flux_sig_i` float,
`ap_mag_raw_i` float,
`flags2_i` int(10) unsigned,
`kron_flux_i` float,
`kron_flux_err_i` float,
`kron_flux_inner_i` float,
`kron_flux_outer_i` float,
`moments_r1_i` float,
`moments_rh_i` float,
`psf_qf_perfect_i` float,
`fpa_filter_i` varchar(80),
`mjd_obs_i` double,
`exptime_i` double,
`imageid_i` int(11),
`zero_pt_i` double,
`delta_mag_i` float,
`no_of_filter_values_i` int,
`ipp_idet_z` int(10) unsigned,
`psf_inst_mag_z` float,
`psf_inst_mag_sig_z` float,
`ap_mag_z` float,
`ap_mag_radius_z` float,
`peak_flux_as_mag_z` float,
`cal_psf_mag_z` float,
`cal_psf_mag_sig_z` float,
`sky_z` float,
`sky_sigma_z` float,
`psf_chisq_z` float,
`cr_nsigma_z` float,
`ext_nsigma_z` float,
`psf_major_z` float,
`psf_minor_z` float,
`psf_theta_z` float,
`psf_qf_z` float,
`psf_ndof_z` int(11),
`psf_npix_z` int(11),
`moments_xx_z` float,
`moments_xy_z` float,
`moments_yy_z` float,
`flags_z` int(10) unsigned,
`n_frames_z` smallint(5) unsigned,
`padding_z` smallint(6),
`psf_inst_flux_z` float,
`psf_inst_flux_sig_z` float,
`ap_flux_z` float,
`ap_flux_sig_z` float,
`ap_mag_raw_z` float,
`flags2_z` int(10) unsigned,
`kron_flux_z` float,
`kron_flux_err_z` float,
`kron_flux_inner_z` float,
`kron_flux_outer_z` float,
`moments_r1_z` float,
`moments_rh_z` float,
`psf_qf_perfect_z` float,
`fpa_filter_z` varchar(80),
`mjd_obs_z` double,
`exptime_z` double,
`imageid_z` int(11),
`zero_pt_z` double,
`delta_mag_z` float,
`no_of_filter_values_z` int,
`ipp_idet_y` int(10) unsigned,
`psf_inst_mag_y` float,
`psf_inst_mag_sig_y` float,
`ap_mag_y` float,
`ap_mag_radius_y` float,
`peak_flux_as_mag_y` float,
`cal_psf_mag_y` float,
`cal_psf_mag_sig_y` float,
`sky_y` float,
`sky_sigma_y` float,
`psf_chisq_y` float,
`cr_nsigma_y` float,
`ext_nsigma_y` float,
`psf_major_y` float,
`psf_minor_y` float,
`psf_theta_y` float,
`psf_qf_y` float,
`psf_ndof_y` int(11),
`psf_npix_y` int(11),
`moments_xx_y` float,
`moments_xy_y` float,
`moments_yy_y` float,
`flags_y` int(10) unsigned,
`n_frames_y` smallint(5) unsigned,
`padding_y` smallint(6),
`psf_inst_flux_y` float,
`psf_inst_flux_sig_y` float,
`ap_flux_y` float,
`ap_flux_sig_y` float,
`ap_mag_raw_y` float,
`flags2_y` int(10) unsigned,
`kron_flux_y` float,
`kron_flux_err_y` float,
`kron_flux_inner_y` float,
`kron_flux_outer_y` float,
`moments_r1_y` float,
`moments_rh_y` float,
`psf_qf_perfect_y` float,
`fpa_filter_y` varchar(80),
`mjd_obs_y` double,
`exptime_y` double,
`imageid_y` int(11),
`zero_pt_y` double,
`delta_mag_y` float,
`no_of_filter_values_y` int,
`object_classification` int unsigned,
`htm20ID` bigint(20) unsigned NOT NULL,
`htm16ID` bigint(20) unsigned NOT NULL,
`cx` double NOT NULL,
`cy` double NOT NULL,
`cz` double NOT NULL,
PRIMARY KEY `key_id` (`id`),
KEY `idx_ipp_idet_g` (`ipp_idet_g`),
KEY `idx_ipp_idet_r` (`ipp_idet_r`),
KEY `idx_ipp_idet_i` (`ipp_idet_i`),
KEY `idx_ipp_idet_z` (`ipp_idet_z`),
KEY `idx_ipp_idet_y` (`ipp_idet_y`),
KEY `idx_htm20ID` (`htm20ID`),
KEY `idx_htm16ID` (`htm16ID`),
KEY `idx_ra_decl` (`ra`,`decl`),
KEY `idx_object_classification` (`object_classification`),
KEY `idx_mdfield` (`mdfield`)
) ENGINE=MyISAM;
