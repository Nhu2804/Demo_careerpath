# career_analysis_html.py

BUSINESS_HTML = """
<div class="header-text">
    <h2>Quản lý – Kinh doanh</h2>
      <p>Bạn có khả năng tổ chức, lãnh đạo và tinh thần cầu tiến, phù hợp với môi trường chuyên nghiệp, năng động và có định hướng mục tiêu rõ ràng.</p>
  </div>
<div class="progress-circle-wrapper" data-score="{score}">
    <svg class="progress-ring" width="100" height="100">
        <circle class="progress-ring-track" stroke-width="8" fill="transparent" r="44" cx="50" cy="50"/>
        <circle class="progress-ring-indicator" stroke-width="8" fill="transparent" r="44" cx="50" cy="50"/>
    </svg>
    <span class="progress-score">{score}%</span>
</div>

<div class="analysis-step-list">

    <!-- Bước 1: Vì sao phù hợp? -->
    <div class="analysis-step">
        <div class="step-visual">
            <div class="step-icon-wrapper icon-bg-teal"><i class="fas fa-user-tie"></i></div>
            <div class="step-line"></div>
        </div>
        <div class="step-content">
            <div class="step-content-card">
                <h6 class="step-title">Vì sao bạn phù hợp?</h6>
                <div class="step-body">
                    <ul class="styled-list-v">
                        <li>Thích lập kế hoạch, tổ chức công việc, quản lý đội nhóm.</li>
                        <li>Quan tâm đến kinh doanh, marketing, phát triển sản phẩm, dịch vụ.</li>
                        <li>Thích giao tiếp, đàm phán, xây dựng mối quan hệ với khách hàng, đối tác.</li>
                        <li>Ưa thử thách bản thân trong môi trường năng động, có mục tiêu cụ thể.</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <!-- Bước 2: Kỹ năng -->
    <div class="analysis-step">
        <div class="step-visual">
            <div class="step-icon-wrapper icon-bg-sky"><i class="fas fa-star"></i></div>
            <div class="step-line"></div>
        </div>
        <div class="step-content">
            <div class="step-content-card">
                <h6 class="step-title">Năng lực & Tiềm năng</h6>
                <div class="step-body">
                    <div class="skills-split-v2">
                        <div class="skill-column">
                            <div class="skill-title"><i class="fas fa-check-circle text-green-500"></i> Kỹ năng nổi bật</div>
                            <p>Giao tiếp, làm việc nhóm, quản lý thời gian, thuyết phục, tư duy phản biện.</p>
                        </div>
                        <div class="skill-column">
                            <div class="skill-title"><i class="fas fa-tools text-orange-500"></i> Cần phát triển thêm</div>
                            <p>Kỹ năng lãnh đạo, quản lý dự án, lập kế hoạch kinh doanh, phân tích tài chính.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Bước 3: Ngành nghề phù hợp -->
    <div class="analysis-step">
        <div class="step-visual">
            <div class="step-icon-wrapper icon-bg-violet"><i class="fas fa-sitemap"></i></div>
            <div class="step-line"></div>
        </div>
        <div class="step-content">
            <div class="step-content-card">
                <h6 class="step-title">Các ngành nghề phù hợp</h6>
                <div class="step-body">
                    <p>Đây là nhóm ngành có nhu cầu lao động cao, cơ hội thăng tiến tốt và tiềm năng phát triển lâu dài.</p>
                    <div class="career-tags">
                        <div class="tag">Quản trị Kinh doanh</div>
                        <div class="tag">Marketing</div>
                        <div class="tag">Quản trị Thương hiệu</div>
                        <div class="tag">Quản lý Dự án</div>
                        <div class="tag">Tài chính – Ngân hàng</div>
                        <div class="tag">Quản trị Nhân sự</div>
                        <div class="tag">Logistics</div>
                        <div class="tag">Khởi nghiệp</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Bước 4: Khóa học gợi ý -->
    <div class="analysis-step">
        <div class="step-visual">
            <div class="step-icon-wrapper icon-bg-rose"><i class="fas fa-graduation-cap"></i></div>
            <div class="step-line"></div>
        </div>
        <div class="step-content">
            <div class="step-content-card">
                <h6 class="step-title">Gợi ý khóa học nên học</h6>
                <div class="step-body">
                    <ul class="styled-list-v">
                        <li>Kỹ năng giao tiếp và đàm phán trong kinh doanh.</li>
                        <li>Kỹ năng lãnh đạo và quản lý đội nhóm.</li>
                        <li>Marketing căn bản và Digital Marketing.</li>
                        <li>Lập kế hoạch và quản lý dự án.</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <!-- Bước 5: Lộ trình -->
    <div class="analysis-step">
        <div class="step-visual">
            <div class="step-icon-wrapper icon-bg-amber"><i class="fas fa-road"></i></div>
        </div>
        <div class="step-content">
            <div class="step-content-card">
                <h6 class="step-title">Lộ trình phát triển gợi ý</h6>
                <div class="step-body">
                    <div class="roadmap-container">
                        <div class="roadmap-step">
                            <div class="roadmap-icon-wrapper"><i class="fas fa-seedling"></i></div>
                            <div class="roadmap-content"><strong>Ngắn hạn (0–6 tháng):</strong> Tham gia CLB kinh doanh, CLB khởi nghiệp; học kỹ năng giao tiếp, bán hàng.</div>
                        </div>
                        <div class="roadmap-step">
                            <div class="roadmap-icon-wrapper"><i class="fas fa-rocket"></i></div>
                            <div class="roadmap-content"><strong>Trung hạn (6–12 tháng):</strong> Tham gia cuộc thi ý tưởng kinh doanh, thực tập tại doanh nghiệp nhỏ.</div>
                        </div>
                        <div class="roadmap-step">
                            <div class="roadmap-icon-wrapper"><i class="fas fa-crown"></i></div>
                            <div class="roadmap-content"><strong>Dài hạn (1–3 năm):</strong> Học ngành phù hợp, thực tập tại công ty, tham gia các khóa kỹ năng lãnh đạo.</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>


<!-- Thẻ kết luận -->
<div class="analysis-conclusion">
    <div class="conclusion-icon"><i class="fas fa-flag-checkered"></i></div>
    <div class="conclusion-text">
        <h6>Tổng kết & Lời khuyên</h6>
        <p>Bạn có tiềm năng phát triển mạnh mẽ trong nhóm ngành <strong>Quản lý – Kinh doanh</strong>. Hãy bắt đầu từ việc rèn luyện các kỹ năng nền tảng và tích cực học hỏi để sẵn sàng cho một tương lai nghề nghiệp thành công.</p>
    </div>
</div>
"""


TECH_HTML = """
  <div class="header-text">
      <h2>Công nghệ – Kỹ thuật</h2>
      <p>Bạn có tư duy logic, yêu thích công nghệ và kiên nhẫn trong việc giải quyết các vấn đề kỹ thuật hoặc phát triển sản phẩm công nghệ.</p>
  </div>
  <div class="progress-circle-wrapper" data-score="{score}">
        <svg class="progress-ring" width="100" height="100">
            <circle class="progress-ring-track" stroke-width="8" fill="transparent" r="44" cx="50" cy="50"/>
            <circle class="progress-ring-indicator" stroke-width="8" fill="transparent" r="44" cx="50" cy="50"/>
        </svg>
        <span class="progress-score">{score}%</span>
  </div>


<div class="analysis-step-list">

    <!-- Bước 1: Vì sao phù hợp? -->
    <div class="analysis-step">
        <div class="step-visual">
            <div class="step-icon-wrapper icon-bg-sky"><i class="fas fa-brain"></i></div>
            <div class="step-line"></div>
        </div>
        <div class="step-content">
            <div class="step-content-card">
                <h6 class="step-title">Vì sao bạn phù hợp?</h6>
                <div class="step-body">
                    <ul class="styled-list-v">
                        <li>Yêu thích làm việc với máy tính, công nghệ và thiết bị kỹ thuật.</li>
                        <li>Hứng thú với lập trình, nghiên cứu và phát triển công nghệ mới.</li>
                        <li>Có tư duy logic, phân tích, giải quyết vấn đề rõ ràng.</li>
                        <li>Kiên nhẫn, tỉ mỉ, sẵn sàng học hỏi và thử nghiệm.</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <!-- Bước 2: Kỹ năng -->
    <div class="analysis-step">
        <div class="step-visual">
            <div class="step-icon-wrapper icon-bg-violet"><i class="fas fa-gears"></i></div>
            <div class="step-line"></div>
        </div>
        <div class="step-content">
            <div class="step-content-card">
                <h6 class="step-title">Năng lực & Tiềm năng</h6>
                <div class="step-body">
                    <div class="skills-split-v2">
                        <div class="skill-column">
                            <div class="skill-title"><i class="fas fa-check-circle text-blue-500"></i> Kỹ năng nổi bật</div>
                            <p>Tư duy logic, phân tích vấn đề, khả năng tập trung, học hỏi nhanh, tự nghiên cứu.</p>
                        </div>
                        <div class="skill-column">
                            <div class="skill-title"><i class="fas fa-tools text-orange-500"></i> Cần phát triển thêm</div>
                            <p>Kỹ năng lập trình, sử dụng công cụ kỹ thuật, làm việc nhóm, tiếng Anh chuyên ngành.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Bước 3: Ngành nghề phù hợp -->
    <div class="analysis-step">
        <div class="step-visual">
            <div class="step-icon-wrapper icon-bg-teal"><i class="fas fa-code-branch"></i></div>
            <div class="step-line"></div>
        </div>
        <div class="step-content">
            <div class="step-content-card">
                <h6 class="step-title">Các ngành nghề phù hợp</h6>
                <div class="step-body">
                    <p>Đây là nhóm ngành đang có nhu cầu nhân lực cao, mức thu nhập tốt và cơ hội phát triển không giới hạn.</p>
                    <div class="career-tags">
                        <div class="tag">Công nghệ Thông tin</div>
                        <div class="tag">Lập trình Phần mềm</div>
                        <div class="tag">Khoa học Dữ liệu</div>
                        <div class="tag">Trí tuệ Nhân tạo</div>
                        <div class="tag">An ninh mạng</div>
                        <div class="tag">Kỹ thuật Cơ khí</div>
                        <div class="tag">Robotics</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Bước 4: Khóa học gợi ý -->
    <div class="analysis-step">
        <div class="step-visual">
            <div class="step-icon-wrapper icon-bg-rose"><i class="fas fa-graduation-cap"></i></div>
            <div class="step-line"></div>
        </div>
        <div class="step-content">
            <div class="step-content-card">
                <h6 class="step-title">Gợi ý khóa học nên học</h6>
                <div class="step-body">
                    <ul class="styled-list-v">
                        <li>Học lập trình (Python, C++, Java cơ bản).</li>
                        <li>Khóa học AI cơ bản và Data Science.</li>
                        <li>Thiết kế mạch điện – Arduino, IoT.</li>
                        <li>Kỹ năng giải quyết vấn đề kỹ thuật.</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <!-- Bước 5: Lộ trình -->
    <div class="analysis-step">
        <div class="step-visual">
            <div class="step-icon-wrapper icon-bg-amber"><i class="fas fa-rocket"></i></div>
        </div>
        <div class="step-content">
            <div class="step-content-card">
                <h6 class="step-title">Lộ trình phát triển gợi ý</h6>
                <div class="step-body">
                    <div class="roadmap-container">
                        <div class="roadmap-step">
                            <div class="roadmap-icon-wrapper"><i class="fas fa-seedling"></i></div>
                            <div class="roadmap-content"><strong>Ngắn hạn (0–6 tháng):</strong> Học lập trình cơ bản, tham gia CLB công nghệ, thực hành các dự án nhỏ.</div>
                        </div>
                        <div class="roadmap-step">
                            <div class="roadmap-icon-wrapper"><i class="fas fa-cogs"></i></div>
                            <div class="roadmap-content"><strong>Trung hạn (6–12 tháng):</strong> Tham gia cuộc thi tin học, robotics, học công cụ kỹ thuật.</div>
                        </div>
                        <div class="roadmap-step">
                            <div class="roadmap-icon-wrapper"><i class="fas fa-user-astronaut"></i></div>
                            <div class="roadmap-content"><strong>Dài hạn (1–3 năm):</strong> Chọn chuyên ngành phù hợp, thực tập tại công ty công nghệ, phát triển kỹ năng chuyên sâu.</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Thẻ kết luận -->
<div class="analysis-conclusion">
    <div class="conclusion-icon"><i class="fas fa-flag-checkered"></i></div>
    <div class="conclusion-text">
        <h6>Tổng kết & Lời khuyên</h6>
        <p>Bạn có tiềm năng phát triển mạnh mẽ trong nhóm ngành <strong>Công nghệ – Kỹ thuật</strong>. Hãy bắt đầu học lập trình, tham gia các dự án thực tế để sẵn sàng cho một tương lai nghề nghiệp ổn định và sáng tạo.</p>
    </div>
</div>
"""


ARTS_HTML = """
<div class="header-text">
    <h2>Sáng tạo – Nghệ thuật</h2>
    <p>Bạn có óc sáng tạo, gu thẩm mỹ và khả năng biểu đạt cảm xúc qua các hình thức nghệ thuật, phù hợp với các ngành nghề yêu cầu sự linh hoạt và đổi mới.</p>
</div>
<div class="progress-circle-wrapper" data-score="{score}">
    <svg class="progress-ring" width="100" height="100">
        <circle class="progress-ring-track" stroke-width="8" fill="transparent" r="44" cx="50" cy="50"/>
        <circle class="progress-ring-indicator" stroke-width="8" fill="transparent" r="44" cx="50" cy="50"/>
    </svg>
    <span class="progress-score">{score}%</span>
</div>

<div class="analysis-step-list">

    <!-- Bước 1: Vì sao phù hợp? -->
    <div class="analysis-step">
        <div class="step-visual">
            <div class="step-icon-wrapper icon-bg-rose"><i class="fas fa-paint-brush"></i></div>
            <div class="step-line"></div>
        </div>
        <div class="step-content">
            <div class="step-content-card">
                <h6 class="step-title">Vì sao bạn phù hợp?</h6>
                <div class="step-body">
                    <ul class="styled-list-v">
                        <li>Yêu thích nghệ thuật, thiết kế, âm nhạc hoặc các hình thức sáng tạo khác.</li>
                        <li>Có khả năng cảm nhận thẩm mỹ tốt và thích làm việc với hình ảnh, màu sắc, âm thanh.</li>
                        <li>Thích thể hiện bản thân qua sản phẩm nghệ thuật, sáng tác nội dung.</li>
                        <li>Luôn tìm tòi cái mới, linh hoạt, không ngại thử nghiệm ý tưởng.</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <!-- Bước 2: Kỹ năng -->
    <div class="analysis-step">
        <div class="step-visual">
            <div class="step-icon-wrapper icon-bg-sky"><i class="fas fa-lightbulb"></i></div>
            <div class="step-line"></div>
        </div>
        <div class="step-content">
            <div class="step-content-card">
                <h6 class="step-title">Năng lực & Tiềm năng</h6>
                <div class="step-body">
                    <div class="skills-split-v2">
                        <div class="skill-column">
                            <div class="skill-title"><i class="fas fa-check-circle text-green-500"></i> Kỹ năng nổi bật</div>
                            <p>Sáng tạo, tư duy hình ảnh, cảm thụ nghệ thuật, linh hoạt trong cách tiếp cận vấn đề.</p>
                        </div>
                        <div class="skill-column">
                            <div class="skill-title"><i class="fas fa-tools text-orange-500"></i> Cần phát triển thêm</div>
                            <p>Kỹ năng kỹ thuật trong thiết kế, sử dụng công cụ sáng tạo, làm việc nhóm, xây dựng thương hiệu cá nhân.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Bước 3: Ngành nghề phù hợp -->
    <div class="analysis-step">
        <div class="step-visual">
            <div class="step-icon-wrapper icon-bg-violet"><i class="fas fa-music"></i></div>
            <div class="step-line"></div>
        </div>
        <div class="step-content">
            <div class="step-content-card">
                <h6 class="step-title">Các ngành nghề phù hợp</h6>
                <div class="step-body">
                    <p>Nhóm ngành sáng tạo – nghệ thuật cho phép bạn phát huy cá tính, mang lại sự hứng thú và nhiều cơ hội phát triển.</p>
                    <div class="career-tags">
                        <div class="tag">Thiết kế Đồ họa</div>
                        <div class="tag">Nghệ thuật Âm nhạc</div>
                        <div class="tag">Thiết kế Thời trang</div>
                        <div class="tag">Truyền thông Đa phương tiện</div>
                        <div class="tag">Nhiếp ảnh</div>
                        <div class="tag">Hoạt hình & Game</div>
                        <div class="tag">Viết lách & Biên tập</div>
                        <div class="tag">Mỹ thuật ứng dụng</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Bước 4: Khóa học gợi ý -->
    <div class="analysis-step">
        <div class="step-visual">
            <div class="step-icon-wrapper icon-bg-rose"><i class="fas fa-graduation-cap"></i></div>
            <div class="step-line"></div>
        </div>
        <div class="step-content">
            <div class="step-content-card">
                <h6 class="step-title">Gợi ý khóa học nên học</h6>
                <div class="step-body">
                    <ul class="styled-list-v">
                        <li>Thiết kế đồ họa cơ bản (Photoshop, Illustrator).</li>
                        <li>Làm video và dựng phim cơ bản.</li>
                        <li>Sáng tác nội dung sáng tạo.</li>
                        <li>Nhiếp ảnh & xử lý hình ảnh.</li>
                        <li>Khóa học về mỹ thuật hoặc nghệ thuật thị giác.</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <!-- Bước 5: Lộ trình -->
    <div class="analysis-step">
        <div class="step-visual">
            <div class="step-icon-wrapper icon-bg-amber"><i class="fas fa-road"></i></div>
        </div>
        <div class="step-content">
            <div class="step-content-card">
                <h6 class="step-title">Lộ trình phát triển gợi ý</h6>
                <div class="step-body">
                    <div class="roadmap-container">
                        <div class="roadmap-step">
                            <div class="roadmap-icon-wrapper"><i class="fas fa-seedling"></i></div>
                            <div class="roadmap-content"><strong>Ngắn hạn (0–6 tháng):</strong> Học công cụ thiết kế cơ bản, tham gia CLB nghệ thuật, bắt đầu xây dựng portfolio cá nhân.</div>
                        </div>
                        <div class="roadmap-step">
                            <div class="roadmap-icon-wrapper"><i class="fas fa-palette"></i></div>
                            <div class="roadmap-content"><strong>Trung hạn (6–12 tháng):</strong> Tham gia các cuộc thi sáng tạo, thực tập tại studio hoặc công ty truyền thông.</div>
                        </div>
                        <div class="roadmap-step">
                            <div class="roadmap-icon-wrapper"><i class="fas fa-star"></i></div>
                            <div class="roadmap-content"><strong>Dài hạn (1–3 năm):</strong> Chọn chuyên ngành nghệ thuật phù hợp, học nâng cao, xây dựng thương hiệu cá nhân trong ngành.</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Thẻ kết luận -->
<div class="analysis-conclusion">
    <div class="conclusion-icon"><i class="fas fa-flag-checkered"></i></div>
    <div class="conclusion-text">
        <h6>Tổng kết & Lời khuyên</h6>
        <p>Bạn có tiềm năng phát triển trong lĩnh vực <strong>Sáng tạo – Nghệ thuật</strong>. Hãy tiếp tục rèn luyện kỹ năng sáng tạo, thử nghiệm các dự án nghệ thuật nhỏ để dần xây dựng phong cách và thương hiệu cá nhân.</p>
    </div>
</div>
"""


HEALTH_HTML = """
<div class="header-text">
    <h2>Y tế – Sức khỏe</h2>
    <p>Bạn có lòng nhân ái, kiên nhẫn và mong muốn đóng góp cho cộng đồng thông qua việc chăm sóc sức khỏe và hỗ trợ người khác.</p>
</div>
<div class="progress-circle-wrapper" data-score="{score}">
    <svg class="progress-ring" width="100" height="100">
        <circle class="progress-ring-track" stroke-width="8" fill="transparent" r="44" cx="50" cy="50"/>
        <circle class="progress-ring-indicator" stroke-width="8" fill="transparent" r="44" cx="50" cy="50"/>
    </svg>
    <span class="progress-score">{score}%</span>
</div>
</div>

<div class="analysis-step-list">

    <!-- Bước 1: Vì sao phù hợp? -->
    <div class="analysis-step">
        <div class="step-visual">
            <div class="step-icon-wrapper icon-bg-rose"><i class="fas fa-heartbeat"></i></div>
            <div class="step-line"></div>
        </div>
        <div class="step-content">
            <div class="step-content-card">
                <h6 class="step-title">Vì sao bạn phù hợp?</h6>
                <div class="step-body">
                    <ul class="styled-list-v">
                        <li>Quan tâm đến sức khỏe, sự an toàn và hạnh phúc của người khác.</li>
                        <li>Kiên nhẫn, trách nhiệm và có khả năng làm việc dưới áp lực.</li>
                        <li>Thích hỗ trợ, lắng nghe và chăm sóc người khác.</li>
                        <li>Có tinh thần phục vụ cộng đồng và mong muốn tạo ra sự thay đổi tích cực.</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <!-- Bước 2: Kỹ năng -->
    <div class="analysis-step">
        <div class="step-visual">
            <div class="step-icon-wrapper icon-bg-sky"><i class="fas fa-hand-holding-medical"></i></div>
            <div class="step-line"></div>
        </div>
        <div class="step-content">
            <div class="step-content-card">
                <h6 class="step-title">Năng lực & Tiềm năng</h6>
                <div class="step-body">
                    <div class="skills-split-v2">
                        <div class="skill-column">
                            <div class="skill-title"><i class="fas fa-check-circle text-green-500"></i> Kỹ năng nổi bật</div>
                            <p>Giao tiếp, chăm sóc người bệnh, làm việc nhóm, xử lý tình huống khẩn cấp.</p>
                        </div>
                        <div class="skill-column">
                            <div class="skill-title"><i class="fas fa-tools text-orange-500"></i> Cần phát triển thêm</div>
                            <p>Kỹ năng y tế chuyên sâu, quản lý thời gian, kỹ năng nghiên cứu, kiến thức về tâm lý học.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Bước 3: Ngành nghề phù hợp -->
    <div class="analysis-step">
        <div class="step-visual">
            <div class="step-icon-wrapper icon-bg-violet"><i class="fas fa-stethoscope"></i></div>
            <div class="step-line"></div>
        </div>
        <div class="step-content">
            <div class="step-content-card">
                <h6 class="step-title">Các ngành nghề phù hợp</h6>
                <div class="step-body">
                    <p>Nhóm ngành y tế – sức khỏe có nhu cầu nhân lực cao, đem lại cơ hội phát triển bền vững và đóng góp tích cực cho cộng đồng.</p>
                    <div class="career-tags">
                        <div class="tag">Y đa khoa</div>
                        <div class="tag">Điều dưỡng</div>
                        <div class="tag">Dược</div>
                        <div class="tag">Tâm lý học</div>
                        <div class="tag">Vật lý trị liệu</div>
                        <div class="tag">Dinh dưỡng</div>
                        <div class="tag">Kỹ thuật xét nghiệm</div>
                        <div class="tag">Y tế cộng đồng</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Bước 4: Khóa học gợi ý -->
    <div class="analysis-step">
        <div class="step-visual">
            <div class="step-icon-wrapper icon-bg-rose"><i class="fas fa-graduation-cap"></i></div>
            <div class="step-line"></div>
        </div>
        <div class="step-content">
            <div class="step-content-card">
                <h6 class="step-title">Gợi ý khóa học nên học</h6>
                <div class="step-body">
                    <ul class="styled-list-v">
                        <li>Sơ cấp cứu cơ bản.</li>
                        <li>Kỹ năng giao tiếp trong y tế.</li>
                        <li>Chăm sóc bệnh nhân cơ bản.</li>
                        <li>Kỹ năng quản lý căng thẳng và áp lực công việc.</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <!-- Bước 5: Lộ trình -->
    <div class="analysis-step">
        <div class="step-visual">
            <div class="step-icon-wrapper icon-bg-amber"><i class="fas fa-road"></i></div>
        </div>
        <div class="step-content">
            <div class="step-content-card">
                <h6 class="step-title">Lộ trình phát triển gợi ý</h6>
                <div class="step-body">
                    <div class="roadmap-container">
                        <div class="roadmap-step">
                            <div class="roadmap-icon-wrapper"><i class="fas fa-seedling"></i></div>
                            <div class="roadmap-content"><strong>Ngắn hạn (0–6 tháng):</strong> Học kỹ năng sơ cấp cứu, tham gia CLB tình nguyện y tế, học kiến thức y tế cơ bản.</div>
                        </div>
                        <div class="roadmap-step">
                            <div class="roadmap-icon-wrapper"><i class="fas fa-heart"></i></div>
                            <div class="roadmap-content"><strong>Trung hạn (6–12 tháng):</strong> Tham gia các hoạt động cộng đồng, thực tập tại các phòng khám, bệnh viện.</div>
                        </div>
                        <div class="roadmap-step">
                            <div class="roadmap-icon-wrapper"><i class="fas fa-user-md"></i></div>
                            <div class="roadmap-content"><strong>Dài hạn (1–3 năm):</strong> Chọn ngành học y tế phù hợp, tham gia các khóa học chuyên sâu, thực tập tại bệnh viện lớn.</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Thẻ kết luận -->
<div class="analysis-conclusion">
    <div class="conclusion-icon"><i class="fas fa-flag-checkered"></i></div>
    <div class="conclusion-text">
        <h6>Tổng kết & Lời khuyên</h6>
        <p>Bạn phù hợp với nhóm ngành <strong>Y tế – Sức khỏe</strong> nhờ sự quan tâm đến cộng đồng và tinh thần trách nhiệm cao. Hãy bắt đầu từ việc tham gia các hoạt động tình nguyện y tế và rèn luyện kỹ năng cần thiết để xây dựng sự nghiệp trong lĩnh vực này.</p>
    </div>
</div>
"""


SOCIAL_HTML = """
<div class="header-text">
    <h2>Xã hội – Nhân văn</h2>
    <p>Bạn yêu thích giao tiếp, hỗ trợ người khác và có mong muốn tạo ra giá trị tích cực cho cộng đồng qua các hoạt động xã hội, giáo dục, và nhân văn.</p>
</div>
<div class="progress-circle-wrapper" data-score="{score}">
    <svg class="progress-ring" width="100" height="100">
        <circle class="progress-ring-track" stroke-width="8" fill="transparent" r="44" cx="50" cy="50"/>
        <circle class="progress-ring-indicator" stroke-width="8" fill="transparent" r="44" cx="50" cy="50"/>
    </svg>
    <span class="progress-score">{score}%</span>
</div>


<div class="analysis-step-list">

    <!-- Bước 1: Vì sao phù hợp? -->
    <div class="analysis-step">
        <div class="step-visual">
            <div class="step-icon-wrapper icon-bg-amber"><i class="fas fa-handshake"></i></div>
            <div class="step-line"></div>
        </div>
        <div class="step-content">
            <div class="step-content-card">
                <h6 class="step-title">Vì sao bạn phù hợp?</h6>
                <div class="step-body">
                    <ul class="styled-list-v">
                        <li>Yêu thích giúp đỡ, chia sẻ và hỗ trợ người khác.</li>
                        <li>Khả năng giao tiếp tốt, dễ đồng cảm và lắng nghe.</li>
                        <li>Quan tâm đến giáo dục, công tác xã hội và phát triển cộng đồng.</li>
                        <li>Đam mê tạo ra giá trị nhân văn và ảnh hưởng tích cực cho xã hội.</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <!-- Bước 2: Kỹ năng -->
    <div class="analysis-step">
        <div class="step-visual">
            <div class="step-icon-wrapper icon-bg-sky"><i class="fas fa-comments"></i></div>
            <div class="step-line"></div>
        </div>
        <div class="step-content">
            <div class="step-content-card">
                <h6 class="step-title">Năng lực & Tiềm năng</h6>
                <div class="step-body">
                    <div class="skills-split-v2">
                        <div class="skill-column">
                            <div class="skill-title"><i class="fas fa-check-circle text-green-500"></i> Kỹ năng nổi bật</div>
                            <p>Giao tiếp, lắng nghe, làm việc nhóm, quản lý thời gian, kỹ năng giảng dạy cơ bản.</p>
                        </div>
                        <div class="skill-column">
                            <div class="skill-title"><i class="fas fa-tools text-orange-500"></i> Cần phát triển thêm</div>
                            <p>Kỹ năng lãnh đạo, kỹ năng tư vấn, quản lý dự án xã hội, kiến thức về tâm lý học.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Bước 3: Ngành nghề phù hợp -->
    <div class="analysis-step">
        <div class="step-visual">
            <div class="step-icon-wrapper icon-bg-teal"><i class="fas fa-users"></i></div>
            <div class="step-line"></div>
        </div>
        <div class="step-content">
            <div class="step-content-card">
                <h6 class="step-title">Các ngành nghề phù hợp</h6>
                <div class="step-body">
                    <p>Nhóm ngành xã hội – nhân văn có tính ổn định, cơ hội phát triển bền vững, phù hợp với những người yêu thích cộng đồng và hỗ trợ người khác.</p>
                    <div class="career-tags">
                        <div class="tag">Giáo dục</div>
                        <div class="tag">Tâm lý học</div>
                        <div class="tag">Công tác xã hội</div>
                        <div class="tag">Truyền thông</div>
                        <div class="tag">Quan hệ công chúng</div>
                        <div class="tag">Luật</div>
                        <div class="tag">Hành chính công</div>
                        <div class="tag">Nhân sự</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Bước 4: Khóa học gợi ý -->
    <div class="analysis-step">
        <div class="step-visual">
            <div class="step-icon-wrapper icon-bg-rose"><i class="fas fa-graduation-cap"></i></div>
            <div class="step-line"></div>
        </div>
        <div class="step-content">
            <div class="step-content-card">
                <h6 class="step-title">Gợi ý khóa học nên học</h6>
                <div class="step-body">
                    <ul class="styled-list-v">
                        <li>Kỹ năng giao tiếp và thuyết trình.</li>
                        <li>Kỹ năng tư vấn và hỗ trợ tâm lý.</li>
                        <li>Kỹ năng làm việc nhóm và quản lý nhóm.</li>
                        <li>Kỹ năng quản lý dự án xã hội.</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <!-- Bước 5: Lộ trình -->
    <div class="analysis-step">
        <div class="step-visual">
            <div class="step-icon-wrapper icon-bg-violet"><i class="fas fa-road"></i></div>
        </div>
        <div class="step-content">
            <div class="step-content-card">
                <h6 class="step-title">Lộ trình phát triển gợi ý</h6>
                <div class="step-body">
                    <div class="roadmap-container">
                        <div class="roadmap-step">
                            <div class="roadmap-icon-wrapper"><i class="fas fa-seedling"></i></div>
                            <div class="roadmap-content"><strong>Ngắn hạn (0–6 tháng):</strong> Tham gia các CLB tình nguyện, rèn luyện kỹ năng giao tiếp, tham gia hoạt động xã hội.</div>
                        </div>
                        <div class="roadmap-step">
                            <div class="roadmap-icon-wrapper"><i class="fas fa-hands-helping"></i></div>
                            <div class="roadmap-content"><strong>Trung hạn (6–12 tháng):</strong> Tham gia các dự án cộng đồng, khóa học kỹ năng mềm, thực tập tại các tổ chức phi lợi nhuận.</div>
                        </div>
                        <div class="roadmap-step">
                            <div class="roadmap-icon-wrapper"><i class="fas fa-user-friends"></i></div>
                            <div class="roadmap-content"><strong>Dài hạn (1–3 năm):</strong> Chọn ngành học phù hợp, thực tập tại các cơ quan giáo dục, tổ chức xã hội, phát triển kỹ năng chuyên sâu.</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

</div>

<!-- Thẻ kết luận -->
<div class="analysis-conclusion">
    <div class="conclusion-icon"><i class="fas fa-flag-checkered"></i></div>
    <div class="conclusion-text">
        <h6>Tổng kết & Lời khuyên</h6>
        <p>Bạn phù hợp với nhóm ngành <strong>Xã hội – Nhân văn</strong> nhờ khả năng giao tiếp, yêu thích hỗ trợ người khác và mong muốn đóng góp cho cộng đồng. Hãy tích cực tham gia các hoạt động xã hội để phát triển kỹ năng và mở rộng cơ hội nghề nghiệp.</p>
    </div>
</div>
"""


SCIENCE_HTML = """
<div class="header-text">
    <h2>Khoa học – Tự nhiên</h2>
    <p>Bạn yêu thích khám phá, nghiên cứu, có tư duy phân tích logic và sự kiên nhẫn, phù hợp với các lĩnh vực nghiên cứu khoa học, công nghệ và tự nhiên.</p>
</div>
<div class="progress-circle-wrapper" data-score="{score}">
    <svg class="progress-ring" width="100" height="100">
        <circle class="progress-ring-track" stroke-width="8" fill="transparent" r="44" cx="50" cy="50"/>
        <circle class="progress-ring-indicator" stroke-width="8" fill="transparent" r="44" cx="50" cy="50"/>
    </svg>
    <span class="progress-score">{score}%</span>
</div>


<div class="analysis-step-list">

    <!-- Bước 1: Vì sao phù hợp? -->
    <div class="analysis-step">
        <div class="step-visual">
            <div class="step-icon-wrapper icon-bg-violet"><i class="fas fa-flask"></i></div>
            <div class="step-line"></div>
        </div>
        <div class="step-content">
            <div class="step-content-card">
                <h6 class="step-title">Vì sao bạn phù hợp?</h6>
                <div class="step-body">
                    <ul class="styled-list-v">
                        <li>Yêu thích tìm hiểu các hiện tượng tự nhiên, khoa học và công nghệ.</li>
                        <li>Khả năng phân tích, quan sát, logic và làm việc chi tiết.</li>
                        <li>Kiên nhẫn trong quá trình nghiên cứu và giải quyết vấn đề.</li>
                        <li>Đam mê khám phá tri thức mới và áp dụng vào thực tiễn.</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <!-- Bước 2: Kỹ năng -->
    <div class="analysis-step">
        <div class="step-visual">
            <div class="step-icon-wrapper icon-bg-sky"><i class="fas fa-microscope"></i></div>
            <div class="step-line"></div>
        </div>
        <div class="step-content">
            <div class="step-content-card">
                <h6 class="step-title">Năng lực & Tiềm năng</h6>
                <div class="step-body">
                    <div class="skills-split-v2">
                        <div class="skill-column">
                            <div class="skill-title"><i class="fas fa-check-circle text-green-500"></i> Kỹ năng nổi bật</div>
                            <p>Tư duy phân tích, quan sát, nghiên cứu, khả năng tập trung và tự học.</p>
                        </div>
                        <div class="skill-column">
                            <div class="skill-title"><i class="fas fa-tools text-orange-500"></i> Cần phát triển thêm</div>
                            <p>Kỹ năng lập kế hoạch nghiên cứu, viết báo cáo khoa học, thuyết trình, kỹ năng làm việc nhóm.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Bước 3: Ngành nghề phù hợp -->
    <div class="analysis-step">
        <div class="step-visual">
            <div class="step-icon-wrapper icon-bg-teal"><i class="fas fa-atom"></i></div>
            <div class="step-line"></div>
        </div>
        <div class="step-content">
            <div class="step-content-card">
                <h6 class="step-title">Các ngành nghề phù hợp</h6>
                <div class="step-body">
                    <p>Nhóm ngành Khoa học – Tự nhiên có tiềm năng nghiên cứu, đóng góp cho sự phát triển xã hội và mở ra nhiều cơ hội nghề nghiệp ổn định.</p>
                    <div class="career-tags">
                        <div class="tag">Khoa học Máy tính</div>
                        <div class="tag">Hóa học</div>
                        <div class="tag">Vật lý</div>
                        <div class="tag">Toán học</div>
                        <div class="tag">Sinh học</div>
                        <div class="tag">Khoa học Môi trường</div>
                        <div class="tag">Địa chất học</div>
                        <div class="tag">Thiên văn học</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Bước 4: Khóa học gợi ý -->
    <div class="analysis-step">
        <div class="step-visual">
            <div class="step-icon-wrapper icon-bg-rose"><i class="fas fa-graduation-cap"></i></div>
            <div class="step-line"></div>
        </div>
        <div class="step-content">
            <div class="step-content-card">
                <h6 class="step-title">Gợi ý khóa học nên học</h6>
                <div class="step-body">
                    <ul class="styled-list-v">
                        <li>Phân tích dữ liệu khoa học (Python, R).</li>
                        <li>Khóa học về phương pháp nghiên cứu khoa học.</li>
                        <li>Khóa học toán cao cấp và xác suất thống kê.</li>
                        <li>Kỹ năng viết báo cáo và trình bày khoa học.</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <!-- Bước 5: Lộ trình -->
    <div class="analysis-step">
        <div class="step-visual">
            <div class="step-icon-wrapper icon-bg-amber"><i class="fas fa-seedling"></i></div>
        </div>
        <div class="step-content">
            <div class="step-content-card">
                <h6 class="step-title">Lộ trình phát triển gợi ý</h6>
                <div class="step-body">
                    <div class="roadmap-container">
                        <div class="roadmap-step">
                            <div class="roadmap-icon-wrapper"><i class="fas fa-leaf"></i></div>
                            <div class="roadmap-content"><strong>Ngắn hạn (0–6 tháng):</strong> Tham gia CLB khoa học, học các kỹ năng phân tích dữ liệu cơ bản.</div>
                        </div>
                        <div class="roadmap-step">
                            <div class="roadmap-icon-wrapper"><i class="fas fa-flask"></i></div>
                            <div class="roadmap-content"><strong>Trung hạn (6–12 tháng):</strong> Tham gia cuộc thi khoa học kỹ thuật, thực tập tại phòng thí nghiệm.</div>
                        </div>
                        <div class="roadmap-step">
                            <div class="roadmap-icon-wrapper"><i class="fas fa-microscope"></i></div>
                            <div class="roadmap-content"><strong>Dài hạn (1–3 năm):</strong> Chọn ngành học phù hợp, tham gia dự án nghiên cứu, phát triển kỹ năng chuyên sâu.</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

</div>

<!-- Thẻ kết luận -->
<div class="analysis-conclusion">
    <div class="conclusion-icon"><i class="fas fa-flag-checkered"></i></div>
    <div class="conclusion-text">
        <h6>Tổng kết & Lời khuyên</h6>
        <p>Bạn phù hợp với nhóm ngành <strong>Khoa học – Tự nhiên</strong> nhờ khả năng phân tích, nghiên cứu và kiên nhẫn trong học tập. Hãy tích cực tham gia các hoạt động nghiên cứu và học tập chuyên sâu để phát triển bản thân trong lĩnh vực này.</p>
    </div>
</div>
"""


# Dictionary tổng
ANALYSIS_HTMLS = {
    "business": BUSINESS_HTML,
    "tech": TECH_HTML,
    "arts": ARTS_HTML,
    "health": HEALTH_HTML,
    "social": SOCIAL_HTML,
    "science": SCIENCE_HTML,
}
